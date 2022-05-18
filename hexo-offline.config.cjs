module.exports = {
    globPatterns: ["**/*.{js,css,webp,png,jpg,gif,svg,eot,ttf,woff,woff2}"],
    globIgnores: ["img/avatar.png", "img/default.png", "img/fluid.png"],
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
            urlPattern: /^https:\/\/utteranc\.es\/.*/,
            handler: "CacheFirst"
        }
    ]
}
