import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

def main():
    datosTrafico = pd.read_csv("Dataset_limpio.csv")
    tablaTrafico = pd.DataFrame(datosTrafico)
    
    # ENCABEZADO DE LA PAGINA
    st.html("<style>h1, h2, p, h3{text-align: center;} .stColumn.st-emotion-cache-1mwoiw6.e1lln2w82{padding: 10px; background: #222; border-radius: 10px;} </style>")
    st.title("🧭 :blue[Navegación Inteligente para una Lima sin Tráfico]",anchor= False)
    st.write(" Descubre la forma más eficiente de moverte por la ciudad, optimizando tu tiempo y reduciendo el estrés.")
    st.divider()
    
    #CUERPO DE LA PAGINA
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("📊", False)
        st.subheader("Predicción Avanzada", False)
        st.write("Modelos predictivos de ultima generación.")
    with col2:
        st.header("🚦", False)
        st.subheader("Análisis en Tiempo Real", False)
        st.write("Información del tráfico al instante.")
    with col3:
        st.header("🗾", False)
        st.subheader("Rutas Inteligentes", False)
        st.write("Las mejores alternativas para tu destino.")
    st.divider()
    
    st.header("Noticias de Tráfico", False)
    st.write("Recuerda revisar las recomendaciones de rutas alternas en nuestra sección de consejos.")
    st.divider()
    
    # MAPA
    cl1, cl2 = st.columns(2)
    with cl1:
        st.subheader("Predicción de Tráfico 🚧", False)
        ubi_start = st.text_input("Desde:", placeholder="Ubicación de inicio.", icon="🚘")
        ubi_end = st.text_input("Hasta:", placeholder="Ubicación de destino.", icon="🏁")
        a = "Callao Callao"
        b = "Lima Peru"
        # Define coordinates for each Zona (approximate)
        coordinates = {
            "Av. Javier Prado": {"lat": -12.0800, "lon": -77.0000},
            "Av. Paseo de la Republica": {"lat": -12.1000, "lon": -77.0300},
            "Av. Alfredo Benavides": {"lat": -12.1300, "lon": -77.0000},
            "Av. Universitaria": {"lat": -12.0200, "lon": -77.0500},
            "Av. de la Marina": {"lat": -12.0600, "lon": -77.0800},
            "Av. Abancay": {"lat": -12.0500, "lon": -77.0300},
            "Av. Mexico": {"lat": -12.0800, "lon": -77.0500},
            "Av. Argentina": {"lat": -12.0500, "lon": -77.0600},
            "Av. Venezuela": {"lat": -12.0600, "lon": -77.0500}
        }
        # Create a DataFrame with unique zones and their coordinates
        zones = datosTrafico["Zona"].unique()
        map_data = pd.DataFrame(
            [{"Zona": zone, "lat": coordinates[zone]["lat"], "lon": coordinates[zone]["lon"]} for zone in zones]
        )
        # Optional: Aggregate FlujoVehicular by Zona (e.g., mean)
        map_data = map_data.merge(
            datosTrafico.groupby("Zona")["FlujoVehicular"].mean().reset_index(),
            on="Zona",
            how="left"
        )
        # Display the map
        st.map(map_data, height= 285)
        
    with cl2:
        res1 = urllib.parse.quote(ubi_start, safe='')
        res2 = urllib.parse.quote(ubi_end, safe='')
        if res1 and res2:
            components.html(f"""
            <div style="border:3px solid #2c3e50; border-radius:20px; overflow:hidden; box-shadow: 0 8px 16px rgba(0,0,0,0.4);">
                <iframe
                    src='https://www.google.com/maps/embed/v1/directions?key=AIzaSyAmBcsfFRbPqws5zmAewz69aw6HGRSVnZc&origin={res1}&destination={res2}=tolls&mode=driving'
                    height="510" width= "100%"
                ></iframe>
            </div>""",height=520)
            
        else:
            components.html("""
                <div style="border:3px solid #2c3e50; border-radius:20px; overflow:hidden; box-shadow: 0 8px 16px rgba(0,0,0,0.4);">
                    <script
                        src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDOd6ZFmKTMdfjLuQ0v66SbN3vnOUdOOMY&libraries=maps,marker"
                        defer
                    ></script>
                    <gmp-map center="37.4220656,-122.0840897" zoom="10" map-id="" style="height: 500px"></gmp-map>
                </div>""", height=520)
    
    # GRAFICOS
    colu1, colu2 = st.columns([0.16,0.84], border=True)
    with colu1:
        st.header("349",anchor= False)
        st.write("max flujo vehicular")
    with colu2:
        f1,f2,f3 = st.columns(3, vertical_alignment = "center")
        with f1:
            st.selectbox("Fecha 📅",("2025-05-10","Mundo"), placeholder="Todas",index=0)
            st.selectbox("Zona 🗾",("Hola","Mundo"), placeholder="Todas",index=None)
        with f2:
            st.selectbox("Feriado 📆",("Hola","Mundo"), placeholder="Todas",index=None)
            st.selectbox("Eventos 🎉",("Hola","Mundo"), placeholder="Todas",index=None)
        with f3:
            st.selectbox("Congestion 🚥",("Hola","Mundo"), placeholder="Todas",index=None)
    # Filtro para una fecha específica (por ejemplo, 1 de mayo de 2025)
    df_filtered = datosTrafico[datosTrafico["Fecha"] == "2025-05-10"]
    # Asignar los datos filtrados
    df_pivot = df_filtered.pivot(index="HoraInicio", columns="Zona", values="FlujoVehicular")
    # Crear el gráfico de áreas
    st.area_chart(df_pivot, width = 900 )
            
    st.dataframe(tablaTrafico, hide_index= True)
if __name__ == "__main__":
    main()
