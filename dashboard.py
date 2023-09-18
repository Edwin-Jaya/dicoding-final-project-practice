import streamlit as st
import pandas
import plotly.express as px
import plotly.graph_objects as go
import folium
import branca
from branca.element import Template, MacroElement
import streamlit.components.v1 as components
st.set_page_config(layout="wide")
st.header('El Edwin Shop Dashboard :sparkles:',divider='rainbow')
container = st.container()
sidebar = st.sidebar
data_jumlah_pembeli_per_kota_tiga_besar=pandas.read_excel("main_data.xlsx",sheet_name="transaksi")
data_rfm = pandas.read_excel("main_data.xlsx",sheet_name="segmentasi_konsumen")
sao_paulo_high_customer = pandas.read_excel("main_data.xlsx",sheet_name="data_barang")
with sidebar:
    st.image("logo.png")
with container:
    colors=["#008000","#32cd32","#7fff00"]
    map_brajil_folium = folium.Map(location=[-21.583799, -44.900], zoom_start=6)
    folium.TileLayer('cartodbpositron').add_to(map_brajil_folium)
    for en in range(len(colors)):
        folium.CircleMarker([data_jumlah_pembeli_per_kota_tiga_besar['lat'][en], data_jumlah_pembeli_per_kota_tiga_besar['long'][en]],
                            fill = True,
                            color = colors[en],
                            radius = 60,
                            fill_opacity=0.6,
                            line_opacity=.1,
                            fill_color = colors[en]).add_to( map_brajil_folium )

    colormap = branca.colormap.LinearColormap([(127, 255, 0, 255), (50, 205, 50, 255), (0, 128, 0, 255)],
                                    vmin=0, vmax=10)
    colormap = colormap.to_step(index=[0, 4000, 8000, 12000, 16000])
    colormap.caption = 'Jumlah Transaksi'
    colormap.add_to(map_brajil_folium)
    textbox_css = """
    {% macro html(this, kwargs) %}
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Testin</title>
        <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css" integrity="sha512-MV7K8+y+gLIBoVD59lQIYicR65iaqukzvf/nwasF0nqhPay5w/9lJmVM2hMDcnK1OnMGCdVK+iQrJ7lzPJQd1w==" crossorigin="anonymous" referrerpolicy="no-referrer"/>
        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

        <script>
        $( function() {
            $( "#textbox" ).draggable({
            start: function (event, ui) {
                $(this).css({
                right: "auto",
                top: "auto",
                bottom: "auto"
                });
            }
            });
        });
        </script>
    </head>

    <body>
        <div id="textbox" class="textbox">
        <div class="textbox-title">Peta 3 Kota Teratas di Brazil Dengan Jumlah Transaksi Terbanyak</div>
        </div>
    
    </body>
    </html>

    <style type='text/css'>
    .textbox {
        position: absolute;
        z-index:9999;
        border-radius:4px;
        background: rgba( 28, 25, 56, 0.25 );
        box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
        backdrop-filter: blur( 4px );
        -webkit-backdrop-filter: blur( 4px );
        border: 4px solid rgba( 215, 164, 93, 0.2 );
        padding: 10px;
        font-size:14px;
        right: 90px;
        bottom: 20px;
        color: orange;
    }
    .textbox .textbox-title {
        color: black;
        text-align: center;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 28px;
        }
    </style>
    {% endmacro %}
    """
    my_custom_style = MacroElement()
    my_custom_style._template = Template(textbox_css)

    map_brajil_folium.get_root().add_child(my_custom_style)
    folium.LayerControl(collapsed=False).add_to(map_brajil_folium)
    html_map = map_brajil_folium._repr_html_()
    components.html(html_map, width=1100, height=800)

#ol1, col2 = st.columns(2,gap="large")
#with col1:
fig = go.Figure()
fig.add_trace(go.Pie(labels=data_rfm["segmen"], 
                    values=data_rfm["jumlah"], 
                    pull=[0, 0.2, 0, 0]))
fig.update_traces(textfont_size=18) 
warna = ["#c4e2c2","#2b4e5e","#78b390","#9acba3"]
fig.update_traces(marker=dict(colors=warna))
fig.update_layout(title='Grafik Segmentasi Customers pada Kota Sao Paulo',
                legend_title_text="Segmentasi Customer",    
                height=690, width=1100,    
                title_font=dict(size=32),
                title_x=0.1,
                    legend=dict(
                                font=dict(size=14),
                                x=-5,  
                                y=0.6   
                                ),
                    legend_title_font=dict(size=20)    

)

st.plotly_chart(fig)

#with col2:
fig = px.bar(sao_paulo_high_customer,
            x=sao_paulo_high_customer["jenis_produk"],
        y=sao_paulo_high_customer["jumlah"],
        color=sao_paulo_high_customer["jumlah"],
        color_continuous_scale=px.colors.sequential.Blugrn,
            labels={"color":"Jumlah Pembelian","x":"Jenis Produk"}, 
            height=690, 
            width=1100,text=sao_paulo_high_customer["jumlah"]
        )
fig.update_layout(
    title='Grafik 5 Produk Terlaris untuk High-Value Costumers di Sao Paulo',
    title_font=dict(size=32),
    title_x=0.10,
    yaxis=dict(
        title='Jumlah Pembelian Produk',
        titlefont_size=18,
        tickfont_size=13.5),
    xaxis=dict(
        titlefont_size=18,
        tickfont_size=16,
        tickangle=90
    )
)
fig.update_traces(textposition="outside",textfont_size=16)
st.plotly_chart(fig)

st.caption('Copyright (c) Edwin Jaya 2023')