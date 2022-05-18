mkdir source/lib
cd source/lib
curl https://cdn.jsdelivr.net/npm/anchor-js@4/anchor.min.js --create-dirs -o anchor-js/anchor.min.js
curl https://cdn.jsdelivr.net/npm/bootstrap@4/dist/css/bootstrap.min.css --create-dirs -o bootstrap/css/bootstrap.min.css
curl https://cdn.jsdelivr.net/npm/bootstrap@4/dist/js/bootstrap.min.js --create-dirs -o bootstrap/js/bootstrap.min.js
curl https://cdn.jsdelivr.net/npm/clipboard@2/dist/clipboard.min.js --create-dirs -o clipboard/clipboard.min.js
curl https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js --create-dirs -o echarts/echarts.min.js
curl https://cdn.jsdelivr.net/gh/apache/echarts-website@asf-site/zh/asset/theme/macarons.min.js --create-dirs -o echarts/macarons.min.js
curl https://cdn.jsdelivr.net/npm/@fancyapps/fancybox@3/dist/jquery.fancybox.min.css --create-dirs -o fancybox/jquery.fancybox.min.css
curl https://cdn.jsdelivr.net/npm/@fancyapps/fancybox@3/dist/jquery.fancybox.min.js --create-dirs -o fancybox/jquery.fancybox.min.js
curl https://cdn.jsdelivr.net/npm/github-markdown-css@4/github-markdown.min.css --create-dirs -o github-markdown-css/github-markdown.min.css
curl https://cdn.jsdelivr.net/npm/jquery@3/dist/jquery.min.js --create-dirs -o jquery/jquery.min.js
curl https://cdn.jsdelivr.net/npm/katex@0/dist/katex.min.css --create-dirs -o katex/katex.min.css
curl https://cdn.jsdelivr.net/npm/mermaid@8/dist/mermaid.min.js --create-dirs -o mermaid/mermaid.min.js
curl https://cdn.jsdelivr.net/npm/no-darkreader@1/nodarkreader.min.js --create-dirs -o nodarkreader/nodarkreader.min.js
curl https://cdn.jsdelivr.net/npm/nprogress@0/nprogress.min.css --create-dirs -o nprogress/nprogress.min.css
curl https://cdn.jsdelivr.net/npm/nprogress@0/nprogress.min.js --create-dirs -o nprogress/nprogress.min.js
curl https://cdn.jsdelivr.net/npm/prismjs@1/components/prism-core.min.js --create-dirs -o prismjs/components/prism-core.min.js
curl https://cdn.jsdelivr.net/npm/prismjs@1/plugins/autoloader/prism-autoloader.min.js --create-dirs -o prismjs/plugins/autoloader/prism-autoloader.min.js
curl https://cdn.jsdelivr.net/npm/prismjs@1/plugins/line-numbers/prism-line-numbers.min.css --create-dirs -o prismjs/plugins/line-numbers/prism-line-numbers.min.css
curl https://cdn.jsdelivr.net/npm/prismjs@1/plugins/line-numbers/prism-line-numbers.min.js --create-dirs -o prismjs/plugins/line-numbers/prism-line-numbers.min.js
curl https://cdn.jsdelivr.net/gh/PrismJS/prism-themes@master/themes/prism-material-light.min.css --create-dirs -o prismjs/themes/prism-material-light.min.css
curl https://cdn.jsdelivr.net/gh/PrismJS/prism-themes@master/themes/prism-material-oceanic.min.css --create-dirs -o prismjs/themes/prism-material-oceanic.min.css
curl https://cdn.jsdelivr.net/npm/tocbot@4/dist/tocbot.min.js --create-dirs -o tocbot/tocbot.min.js
curl https://cdn.jsdelivr.net/npm/typed.js@2/lib/typed.min.js --create-dirs -o typed.js/typed.min.js
find . -type f -exec sed -i '/sourceMappingURL/d' {} \;
find . -type f -exec sed -i '1i\{% raw %}' {} \;
find . -type f -exec sed -i '$a\{% endraw %}' {} \;
