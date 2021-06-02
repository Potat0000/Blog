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
            urlPattern: /^https:\/\/utteranc\.es\/.*/,
            handler: "CacheFirst"
        },
        {
            urlPattern: /^https:\/\/www\.google-analytics\.com\/.*/,
            handler: "NetworkFirst"
        }
    ]
}
