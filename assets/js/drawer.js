// assets/js/drawer.js

document.addEventListener("DOMContentLoaded", () => {
  const logoBtn = document.getElementById("logoBtn");
  const drawer = document.getElementById("drawer");
  const pageWrap = document.getElementById("pageWrap");
  const closeBtn = document.getElementById("drawerClose");

  if (!drawer || !pageWrap) return;

  function openDrawer() {
    drawer.classList.add("open");
    pageWrap.classList.add("shifted");
  }

  function closeDrawer() {
    drawer.classList.remove("open");
    pageWrap.classList.remove("shifted");
  }

  if (logoBtn) {
    logoBtn.addEventListener("click", () => {
      const isHome = window.location.pathname === "/";

      if (!isHome) {
        window.location.href = "/?menu=open";
        return;
      }

      drawer.classList.contains("open") ? closeDrawer() : openDrawer();
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener("click", closeDrawer);
  }

  // Auto-open drawer if coming home from another page
  if (window.location.search.includes("menu=open")) {
    openDrawer();
  }
});
