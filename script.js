const header = document.querySelector("[data-header]");
const menuButton = document.querySelector("[data-menu-button]");
const mobileNav = document.querySelector("[data-mobile-nav]");
const copyButton = document.querySelector("[data-copy-email]");
const email = "hello@linchuan.design";

function renderIcons() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

function updateHeader() {
  header?.classList.toggle("is-scrolled", window.scrollY > 24);
}

function closeMenu() {
  if (!menuButton || !mobileNav) return;

  mobileNav.hidden = true;
  menuButton.setAttribute("aria-expanded", "false");
  menuButton.setAttribute("aria-label", "打开导航菜单");
  menuButton.innerHTML = '<i data-lucide="menu" aria-hidden="true"></i>';
  header?.classList.remove("is-menu-open");
  document.body.classList.remove("menu-open");
  renderIcons();
}

function openMenu() {
  if (!menuButton || !mobileNav) return;

  mobileNav.hidden = false;
  menuButton.setAttribute("aria-expanded", "true");
  menuButton.setAttribute("aria-label", "关闭导航菜单");
  menuButton.innerHTML = '<i data-lucide="x" aria-hidden="true"></i>';
  header?.classList.add("is-menu-open");
  document.body.classList.add("menu-open");
  renderIcons();
}

menuButton?.addEventListener("click", () => {
  const isOpen = menuButton.getAttribute("aria-expanded") === "true";
  isOpen ? closeMenu() : openMenu();
});

mobileNav?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", closeMenu);
});

window.addEventListener("scroll", updateHeader, { passive: true });
window.addEventListener("resize", () => {
  if (window.innerWidth > 900) closeMenu();
});
updateHeader();

document.querySelectorAll("[data-filter]").forEach((button) => {
  button.addEventListener("click", () => {
    const selected = button.dataset.filter;

    document.querySelectorAll("[data-filter]").forEach((item) => {
      const active = item === button;
      item.classList.toggle("is-active", active);
      item.setAttribute("aria-pressed", String(active));
    });

    document.querySelectorAll("[data-category]").forEach((project) => {
      project.hidden = selected !== "all" && project.dataset.category !== selected;
    });
  });
});

copyButton?.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(email);
    copyButton.innerHTML = '<i data-lucide="check" aria-hidden="true"></i><span>已复制</span>';
    renderIcons();
    window.setTimeout(() => {
      copyButton.innerHTML = '<i data-lucide="copy" aria-hidden="true"></i><span>复制邮箱</span>';
      renderIcons();
    }, 1800);
  } catch {
    window.location.href = `mailto:${email}`;
  }
});

document.querySelector("[data-year]").textContent = new Date().getFullYear();

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.14 }
);

document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));
window.addEventListener("DOMContentLoaded", renderIcons);
