// for Previewing and zoomin of grqphs
let zoom = 1;

const modal = document.getElementById("imgModal");
const modalImg = document.getElementById("modalImg");

// zoom handler
modalImg.addEventListener("wheel", (e) => {
    e.preventDefault();

    zoom += e.deltaY * -0.001;
    zoom = Math.min(Math.max(zoom, 1), 5);

    modalImg.style.transform = `scale(${zoom})`;
});

function openModal(img) {
    modal.style.display = "block";
    modalImg.src = img.src;

    zoom = 1; // reset zoom state
    modalImg.style.transform = "scale(1)";
}

// close button
document.querySelector(".close").onclick = function () {
    document.getElementById("imgModal").style.display = "none";
};

// click outside image closes
window.onclick = function (event) {
    const modal = document.getElementById("imgModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
};

// ESC key close
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        document.getElementById("imgModal").style.display = "none";
    }
});

// -------------------------------------------------------------------

