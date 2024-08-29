document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.querySelector(".sidebar");
    const logo = document.querySelector(".image-text");
    const sidebarBtn = document.querySelector(".bx-menu");
    const userInfo = document.querySelector(".user-info");
    const main = document.querySelector(".main");

    const users = document.querySelectorAll('.user');
    const usernameInput = document.getElementById('id_user');
    const formContainer = document.getElementById('userForm');

    const notification = document.querySelector(".notification");
    const bx_notifications = document.querySelector(".bx-notification");

    if (notification) {
        notification.addEventListener("click", function() {
            if (bx_notifications.style.display === "none") {
                bx_notifications.style.display = "flex";
            }
            else {
                bx_notifications.style.display = "none";
            }
        });
    } else {
        console.error('Notification not found');
    }

    if (formContainer && usernameInput) {
        users.forEach(user => {
            user.addEventListener('dragstart', function (event) {
                event.dataTransfer.setData('text', event.target.getAttribute('data-username'));
                event.dataTransfer.setData('userId', event.target.getAttribute('data-user-id'));
            });
        });

        formContainer.addEventListener('dragover', function (event) {
            event.preventDefault();
        });

        formContainer.addEventListener('drop', function (event) {
            event.preventDefault();
            const username = event.dataTransfer.getData('text');
            const userId = event.dataTransfer.getData('userId');

            usernameInput.value = userId;

            const selectElement = document.getElementById('id_user');
            const options = selectElement.options;

            for (let i = 0; i < options.length; i++) {
                if (options[i].value === userId) {
                    selectElement.selectedIndex = i;
                    break;
                }
            }
        });
    } else {
        console.error('Form container or username input not found');
    }


    if (sidebar ) {
        sidebarBtn.addEventListener("click", function() {
        sidebar.classList.toggle("hidden");
        logo.classList.toggle("close");
        userInfo.classList.toggle("destroy");
        main.classList.toggle("clear");
    })
    }
    else {
        console.error('Sidebar, logo, sidebar button, user info, or main not found');
    }
})