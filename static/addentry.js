function addEntry(containerId) {
    const container = document.getElementById(containerId);
    const box = container.children[0].cloneNode(true);
    box.querySelectorAll("input, select").forEach(el => el.value = "");
    container.appendChild(box);
}
const addTraining = () => addEntry("training-container");
const addRecovery = () => addEntry("recovery-container");
const addGoals = () => addEntry("goals-container");
