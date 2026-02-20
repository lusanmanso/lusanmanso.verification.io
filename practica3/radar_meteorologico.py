def alcance_del_radar(T: float, tau: float) -> float:
    """Calcula el alcance del radar meteorológico"""
    """ entrada: T, intervalo de repetición de pulsos [segundos]"""
    """ Entrada: tau, ancho del pulso [microsegundos]"""
    """ Salida: Alcance del radar meteorológico [kilómetros]"""
   
    #se ponen todas lass unidades en segundos, solo en necesario tau, T ya lo está
    tau=tau/pow(10,6)

    Co=3*pow(10,5) #Velocidad de la luz, 300000 km/s
    return Co*(T-tau)/2 # Calculo del alcance de radar
    
