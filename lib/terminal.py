from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

import os
import pty
import select
import subprocess
import threading
import uuid
import signal

terminal_bp = Blueprint(
    'terminal',
    __name__,
    template_folder='templates',
    static_folder='static'
)

# Stores active shell sessions
terminal_sessions = {}

class TerminalSession:
    def __init__(self):
        self.session_id = str(uuid.uuid4())

        self.master_fd, self.slave_fd = pty.openpty()

        env = os.environ.copy()
        env['TERM'] = 'xterm-256color'

        self.process = subprocess.Popen(
            ['/bin/bash'],
            stdin=self.slave_fd,
            stdout=self.slave_fd,
            stderr=self.slave_fd,
            start_new_session=True,
            env=env,
            cwd=os.path.expanduser('~')
        )

        self.buffer = ''
        self.running = True

        self.thread = threading.Thread(target=self.read_output)
        self.thread.daemon = True
        self.thread.start()

    def read_output(self):
        while self.running:
            try:
                ready, _, _ = select.select([self.master_fd], [], [], 0.1)

                if self.master_fd in ready:
                    data = os.read(self.master_fd, 4096)

                    if not data:
                        break

                    self.buffer += data.decode(errors='ignore')

            except Exception:
                break

    def write(self, command):
        os.write(self.master_fd, command.encode())

    def read_buffer(self):
        data = self.buffer
        self.buffer = ''
        return data

    def cleanup(self):
        self.running = False

        try:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
        except Exception:
            pass

        try:
            os.close(self.master_fd)
            os.close(self.slave_fd)
        except Exception:
            pass


@terminal_bp.route('/terminal')
@login_required
def terminal_page():
    if current_user.role != 'admin':
        return 'Forbidden', 403

    return render_template('terminal.html')


@terminal_bp.route('/terminal/create', methods=['POST'])
@login_required
def create_terminal():
    if current_user.role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    session = TerminalSession()

    terminal_sessions[session.session_id] = session

    return jsonify({
        'session_id': session.session_id
    })


@terminal_bp.route('/terminal/input', methods=['POST'])
@login_required
def terminal_input():
    if current_user.role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    data = request.json

    session_id = data.get('session_id')
    command = data.get('command', '')

    session = terminal_sessions.get(session_id)

    if not session:
        return jsonify({'error': 'Session not found'}), 404

    session.write(command)

    return jsonify({'success': True})


@terminal_bp.route('/terminal/output/<session_id>')
@login_required
def terminal_output(session_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    session = terminal_sessions.get(session_id)

    if not session:
        return jsonify({'error': 'Session not found'}), 404

    return jsonify({
        'output': session.read_buffer()
    })


@terminal_bp.route('/terminal/close/<session_id>', methods=['POST'])
@login_required
def close_terminal(session_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    session = terminal_sessions.pop(session_id, None)

    if session:
        session.cleanup()

    return jsonify({'success': True})