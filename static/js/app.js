document.addEventListener("DOMContentLoaded", function () {
  const shareButton = document.getElementById("shareButton");
  const shareModal = document.getElementById("shareModal");
  const closeModal = document.getElementById("closeModal");
  const linksContainer = document.getElementById("linksContainer");

  const telegramIdElement = document.getElementById("telegram_id");
  const usernameElement = document.getElementById("username");
  const firstNameElement = document.getElementById("first_name");
  const lastNameElement = document.getElementById("last_name");
  const languageCodeElement = document.getElementById("language_code");
  const userInfoContainer = document.getElementById("userInfoContainer");
  const loadingIndicator = document.getElementById("loadingIndicator");

  function fetchUserSubscriptionLinks() {
    let tg = window.Telegram.WebApp;
    let user = tg.initDataUnsafe.user;

    if (user) {
      let userData = {
        id: user.id,
        username: user.username || "...",
        first_name: user.first_name || "...",
        last_name: user.last_name || "...",
        language_code: user.language_code || "...",
      };

      loadingIndicator.classList.remove("hidden");
      userInfoContainer.classList.add("hidden");

      fetch("/store_user_info/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      })
        .then(response => response.json())
        .then(data => {
          loadingIndicator.classList.add("hidden");
          userInfoContainer.classList.remove("hidden");

          telegramIdElement.innerText = data.id;
          usernameElement.innerText = data.username;
          firstNameElement.innerText = data.first_name;
          lastNameElement.innerText = data.last_name;
          languageCodeElement.innerText = data.language_code;

          linksContainer.innerHTML = "";
          if (!data.links || data.links.length === 0) {
            linksContainer.innerHTML = `<p class="text-zinc-300 text-center">No links available.</p>`;
            return;
          }

          data.links.forEach((entry, index) => {
            const uniqueId = `website-url-${index}`;
            const uniqueTooltipId = `tooltip-website-url-${index}`;

            const linkWrapper = document.createElement("div");
            linkWrapper.innerHTML = `
              <!-- Link entry template -->
              <div class="w-full max-w-sm">
                <div class="flex items-center">
                  <!-- Username field -->
                  <span
                    class="shrink-0 z-10 inline-flex items-center py-2.5 px-2 text-sm font-medium text-center text-zinc-900 bg-gray-500 rounded-s-lg border border-zinc-200">
                    ${entry.username || "Unknown User"}</span>
                  <!-- Link field -->
                  <div class="relative w-full">
                    <input id="${uniqueId}" type="text"
                      class="bg-zinc-200 border border-e-0 border-zinc-300 text-gray-500 text-sm border-s-0 block w-full p-2.5"
                      value="${entry.link}" readonly />
                  </div>
                  <!-- Copy button -->
                  <button data-tooltip-target="${uniqueTooltipId}" data-copy-to-clipboard-target="${uniqueId}"
                    class="shrink-0 z-10 inline-flex items-center py-3 px-4 text-sm font-medium text-center text-zinc-900 hover:text-zinc-700 bg-zinc-300 border border-zinc-200 rounded-e-lg"
                    type="button">
                    <span class="default-icon">
                      <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 18 20">
                        <path
                          d="M16 1h-3.278A1.992 1.992 0 0 0 11 0H7a1.993 1.993 0 0 0-1.722 1H2a2 2 0 0 0-2 2v15a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2Zm-3 14H5a1 1 0 0 1 0-2h8a1 1 0 0 1 0 2Zm0-4H5a1 1 0 0 1 0-2h8a1 1 0 1 1 0 2Zm0-5H5a1 1 0 0 1 0-2h2V2h4v2h2a1 1 0 1 1 0 2Z" />
                      </svg>
                    </span>
                    <span class="success-icon hidden">
                      <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 12">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M1 5.917 5.724 10.5 15 1.5" />
                      </svg>
                    </span>
                  </button>
                  <!-- Copy tooltip -->
                  <div id="${uniqueTooltipId}" role="tooltip"
                    class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-bold text-zinc-900 transition-opacity duration-300 bg-red-500 rounded-lg shadow-xs opacity-0 tooltip">
                    <span class="default-tooltip-message">Copy link</span>
                    <span class="success-tooltip-message hidden">Copied!</span>
                    <div class="tooltip-arrow" data-popper-arrow></div>
                  </div>
                </div>
              </div>
            `;
            linksContainer.appendChild(linkWrapper);
          });

          initializeClipboard();
        })
        .catch(error => {
          console.error("Error fetching links:", error);
        });
    }
  }

  function initializeClipboard() {
    document.querySelectorAll("[data-copy-to-clipboard-target]").forEach((button) => {
      const targetId = button.getAttribute("data-copy-to-clipboard-target");
      const tooltipId = button.getAttribute("data-tooltip-target");

      const inputField = document.getElementById(targetId);
      const tooltip = document.getElementById(tooltipId);
      const defaultIcon = button.querySelector(".default-icon");
      const successIcon = button.querySelector(".success-icon");
      const defaultTooltipMessage = tooltip.querySelector(".default-tooltip-message");
      const successTooltipMessage = tooltip.querySelector(".success-tooltip-message");

      button.addEventListener("click", function () {
        navigator.clipboard.writeText(inputField.value).then(() => {
          defaultIcon.classList.add("hidden");
          successIcon.classList.remove("hidden");
          defaultTooltipMessage.classList.add("hidden");
          successTooltipMessage.classList.remove("hidden");
          tooltip.classList.remove("invisible");
          tooltip.classList.add("opacity-100");

          setTimeout(() => {
            defaultIcon.classList.remove("hidden");
            successIcon.classList.add("hidden");
            defaultTooltipMessage.classList.remove("hidden");
            successTooltipMessage.classList.add("hidden");
            tooltip.classList.add("invisible");
            tooltip.classList.remove("opacity-100");
          }, 2000);
        });
      });
    });
  }

  fetchUserSubscriptionLinks();
  shareButton.addEventListener("click", () => shareModal.classList.remove("hidden"));
  closeModal.addEventListener("click", () => shareModal.classList.add("hidden"));
});
