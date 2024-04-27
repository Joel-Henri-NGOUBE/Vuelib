
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

// function updateFavoriteStation(code) {
//     const stationData = {
//         action: "remove",
//         stationcode: code
//     };
  
//     let parentButton = document.querySelector(`button[onclick="removeFavoriteStation('${code}')"]`).parentElement
    
//     parentButton.parentElement.removeChild(parentButton)

//     fetch('/favorites', {
//         method: 'POST',
//         headers: {
//             'Content-type': 'application/json'
//         },
//         body: JSON.stringify(stationData)
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log(data);
//     })
//     .catch(error => console.error('Error:', error));
    
// }