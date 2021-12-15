//过滤HTML标签
function removeHTMLTag(str) {
　　　str = str.replace(/<\/?[^>]*>/g, ''); //去除HTML tag
　　　str = str.replace(/[ | ]*\n/g, '\n'); //去除行尾空白
　　　str = str.replace(/\n[\s| | ]*\r/g,'\n'); //去除多余空行
　　　str = str.replace(/ /ig, ''); //去掉
　　　return str;
}