SELECT * FROM Trajets
INNER JOIN LienTrajetStation ON Trajets.id_trajets = LienTrajetStation.id_trajets
INNER JOIN Station ON LienTrajetStation.id_station = Station.id_station