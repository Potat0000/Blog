module.exports = {
    globPatterns: ["**/*.{html,js,css,webp,png,jpg,gif,svg,eot,ttf,woff,woff2}"],
    globIgnores: ["img/avatar.png", "img/default.png", "img/favicon.png", "lib/hint/hint.min.css"],
    globDirectory: "./public",
    runtimeCaching: [
        {
            urlPattern: /^https:\/\/at\.alicdn\.cn\/.*/,
            handler: "CacheFirst"
        },
        {
            urlPattern: /^https:\/\/www\.google-analytics\.com\/.*/,
            handler: "NetworkFirst"
        },
        {
            urlPattern: /^https:\/\/cdn\.jsdelivr\.net\/.*/,
            handler: "CacheFirst"
        },
        {
            urlPattern: /^https:\/\/utteranc\.es\/.*/,
            handler: "CacheFirst"
        }
    ]
}
