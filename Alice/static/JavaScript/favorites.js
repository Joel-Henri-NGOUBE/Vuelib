// Pour ajouter une nouvelles stations
function addFavoriteStation(name,code){
  const stationData={
    name:name,
    stationcode:code
  };
  fetch('/favorites',{
    method:'POST',
    headers:{
      'Content-type': 'application/json'
    },
    body:JSON.stringify(stationData)
  })
  .then(reponse=> response.json())
  .then(data=>{
    console.log(data);
    fetchFavoriteStations();
  })
  .catch(error=> console.error('Error:',error));
}

// Fonction pour voir les stations favoris
function fetchFavoriteStations() {
    fetch('/favorites')
         .then(response=> response.json())
        .then(data => {
            const favoriteStations = data.results;

            updateFavoriteStations(favoriteStations);
        });
}

// fonction pour modifier
function updateFavoriteStations(favoriteStations) {
    const favoriteStationsElement = document.getElementById('favorite-stations');
    favoriteStationsElement.innerHTML = '';
    favoriteStations.forEach(station => {
        const stationElement = document.createElement('div');
        stationElement.innerHTML = `<p>${station.name} - ${station.stationcode}</p>`;
        favoriteStationsElement.appendChild(stationElement);
    });
}

// Fonction pour supprimer 
function deleteFavoriteStation(stationId) {
    fetch(`/favorites/${stationId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
     
        fetchFavoriteStations();
    })
    .catch(error => console.error('Error:', error));
}

