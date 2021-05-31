module.exports = {
    globDirectory: ".github/workflows",
    runtimeCaching: [
        {
            urlPattern: /^https:\/\/cdn\.jsdelivr\.net\/.*/,
            handler: "CacheFirst"
        },
        {
            urlPattern: /^https:\/\/at\.alicdn\.cn\/.*/,
            handler: "CacheFirst"
        },
        {
            urlPattern: /^https:\/\/busuanzi\.ibruce\.info\/.*/,
            handler: "NetworkOnly"
        },
        {
            urlPattern: /^https:\/\/www\.google-analytics\.com\/.*/,
            handler: "NetworkOnly"
        }
    ]
}
