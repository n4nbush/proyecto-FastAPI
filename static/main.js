       function toggleFiltros(){
            console.log("mostrando filtros avanzados")
            document.getElementById('filtros_avanzados').classList.toggle('oculto');
            
            if ((document.getElementById('boton_filtros_avanzados').textContent) != 'Filtros Avanzado▼') {
                document.getElementById('boton_filtros_avanzados').textContent = 'Filtros Avanzado▼';
            }else{
                document.getElementById('boton_filtros_avanzados').textContent = 'Filtros Avanzado▲';
            }
         

        }
        function resumenes(){
            document.getElementById('menu').classList.toggle('oculto');
            if ((document.getElementById('boton_resumenes').textContent) != 'Menu▼') {
                document.getElementById('boton_resumenes').textContent = 'Menu▼';
            }else{
                document.getElementById('boton_resumenes').textContent = 'Menu▲';
            }
        }