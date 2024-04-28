function map(donnee){

    let donnees = donnee
    
     console.log(donnees)
     var map = L.map('map');
     map.setView([48.8534, 2.3488], 25); 
 
     L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
         maxZoom: 14,
         attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
     }).addTo(map);
 
 
 // Ici je vais pouvoir connaitre ma position sur la map 
    //  navigator.geolocation.watchPosition(success, error);
 
     let marker, circle, zoomed;
 
     function success(pos) {
 
         const latitude = pos.coords.latitude;
         const longitude = pos.coords.longitude;
         const accuracy = pos.coords.accuracy;
 
         if (marker) {
             map.removeLayer(marker);
             map.removeLayer(circle);
 
         }
 
         marker = L.marker([latitude, longitude]).addTo(map);
         circle = L.circle([latitude, longitude], {radius: accuracy}).addTo(map);
 
 
         if (!zoomed) {
             zoomed = map.fitBounds(circle.getBounds());
         }
 
         map.setView([latitude, longitude])
     }
 
     function error(err){
 
         if(err.code === 1) {
             alert("Please allow geolocation accesss");
         } else {
             alert("Cannot get current location");
         }
 
     }
        // console.log(donnee.results[0].coordonnees_geo.lat)
        // console.log(donnee.results[0].coordonnees_geo.lon)

        donnee.map((result)=>{
            L.marker([result.coordonnees_geo.lat, result.coordonnees_geo.lon]).addTo(map)
            // .bindPopup(<p>result.name</p> + '<br>'+ result.capacity)
            .bindPopup(`
            <span style="color:#071F32 "><b>${result.name}</b></span>
            <br> <i>${result.nom_arrondissement_communes}</i>
            <hr> <b>Capacité: </b>${result.capacity}
            <br> <b>Emplacements disponibles : </b>${result.numdocksavailable} 
            <br> <b>Vélos disponibles : </b>${result.numbikesavailable}
            <br> <b>Vélos mécaniques : </b>${result.mechanical}
            <br> <b>Vélos électriques : </b>${result.ebike}
            `).openPopup()
            L.circle([result.coordonnees_geo.lat, result.coordonnees_geo.lon], {radius: 1}).addTo(map);
        })
        
}