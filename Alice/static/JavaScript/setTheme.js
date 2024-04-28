function getURI(url, testURL){
    let splitted = url.split(testURL)[0]
    if(splitted !== testURL){
        url = url.replace(splitted, "")
        return url
    }
    return null
}

function setTheme(light_theme, dark_theme){
        let url = document.querySelector("link").href
        let light_theme_url = getURI(url, light_theme)
        let dark_theme_url = getURI(url, dark_theme)
        if(light_theme_url){
            url = light_theme_url
        }
        if(dark_theme_url){
            url = dark_theme_url
        }
        if(url === light_theme){
            document.querySelector("link").href = dark_theme
            document.cookie = "theme=dark"
        }
        if(url === dark_theme){
            document.querySelector("link").href = light_theme
            document.cookie = "theme=light"
    }
}
