
function removeFavoriteStation(code) {
    const stationData = {
        action: "remove",
        stationcode: code
    };
  
    let parentButton = document.querySelector(`button[onclick="removeFavoriteStation('${code}')"]`).parentElement
    
    parentButton.parentElement.removeChild(parentButton)

    fetch('/favorites', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify(stationData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error('Error:', error));
    
}

function commitUpdateFavoriteStation(code, title = "") {
    
    let buttonModify = document.querySelector(`button[onclick="commitUpdateFavoriteStation('${code}')"]`)

    if (title){
        buttonModify = document.querySelector(`button[onclick="commitUpdateFavoriteStation('${code}','${title}')"]`)
    }

    let parentButton = buttonModify.parentElement

    parentButtonContent = parentButton.innerHTML

    // console.log(parentButtonContent.replaceAll("\"","\\\""))
    // "".replaceAll()

    parentButton.innerHTML = `<span>Donnez un nom ou modifiez le nom de cette station</span><br><form class="modify_station" method="POST" action="/favorites"><input type='text' name='title' placeholder="modifier le nom de votre station favorite" value='${title}'><input type="hidden" value="${code}" name="stationcode"><button>Modifier</button></form><br>${parentButtonContent}`
    // parentButton.innerHTML = `<p>Donnez un nom ou modifiez le nom de cette station</p><br><input type='text' name='title'><button onclick="updateFavoriteStation('${code}','${parentButtonContent.replaceAll("\"","`").replaceAll("\n","").replaceAll("'","\\'")}')">Modifier</button><br>${parentButtonContent}`

    // console.log(parentButtonContent.replaceAll("\"","`").replaceAll("\n","").replaceAll("'","\\'"))

    buttonModify = document.querySelector(`button[onclick="commitUpdateFavoriteStation('${code}')"]`)

    if (title){
        buttonModify = document.querySelector(`button[onclick="commitUpdateFavoriteStation('${code}','${title}')"]`)
    }
    
    let buttonDelete = document.querySelector(`button[onclick="removeFavoriteStation('${code}')"]`)
    
    parentButton = buttonModify.parentElement

    parentButton.removeChild(buttonModify)

    parentButton.removeChild(buttonDelete)
}
