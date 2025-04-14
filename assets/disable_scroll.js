function applyScrollRule() {
    const path = window.location.pathname;

    if (path === "/profile") {
        document.documentElement.style.overflowY = "hidden";
        document.body.style.overflowY = "hidden";
    } else {
        document.documentElement.style.overflowY = "auto";
        document.body.style.overflowY = "auto";
    }
}

// Sayfa ilk yüklendiğinde uygula
window.addEventListener("load", applyScrollRule);

// URL değiştiğinde tekrar kontrol et
window.addEventListener("popstate", applyScrollRule);
window.addEventListener("hashchange", applyScrollRule);

// Yedek olarak her 500ms'de bir kontrol et
setInterval(applyScrollRule, 500);
