// Pour ajouter une nouvelles stations

function addFavoriteStation(code) {
  const stationData = {
      action: "add",
      stationcode: code
  };

  let button = document.querySelector(`button[onclick="addFavoriteStation('${code}')"]`)
  if(button.innerHTML == "Ajouter aux favoris"){
      button.outerHTML = `<button onclick="removeFavoriteStation('${code}')">Enlever des favoris</button>`
  }
  else{
      button.outerHTML = `<button onclick="addFavoriteStation('${code}')">Ajouter aux favoris</button>`
  }

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

function removeFavoriteStation(code) {
  const stationData = {
      action: "remove",
      stationcode: code
  };

  let button = document.querySelector(`button[onclick="removeFavoriteStation('${code}')"]`)
  if(button.innerHTML == "Ajouter aux favoris"){
      button.outerHTML = `<button onclick="removeFavoriteStation('${code}')">Enlever des favoris</button>`
  }
  else{
      button.outerHTML = `<button onclick="addFavoriteStation('${code}')">Ajouter aux favoris</button>`
  }

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