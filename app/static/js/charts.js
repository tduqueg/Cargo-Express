const labelsHoras = {{ labels_horas | tojson }};
const datasetsEntregas = {{ datasets_entregas | tojson }};

const ctxEntregas = document.getElementById('entregasPorHoraChart').getContext('2d');
const entregasPorHoraChart = new Chart(ctxEntregas, {
    type: 'bar',
    data: {
        labels: labelsHoras,
        datasets: datasetsEntregas.map(ds => ({
            label: ds.label,
            data: ds.data,
            backgroundColor: getRandomColor(),
            borderColor: getRandomColor(),
            borderWidth: 1
        }))
    },
    options: {
        responsive: true,
        scales: {
            x: {
                stacked: true
            },
            y: {
                beginAtZero: true,
                stacked: true
            }
        }
    }
});

// Datos para productos más vendidos
const labelsProductos = {{ labels_productos | tojson }};
const dataProductos = {{ data_productos | tojson }};

const ctxProductos = document.getElementById('productosMasVendidosChart').getContext('2d');
const productosMasVendidosChart = new Chart(ctxProductos, {
    type: 'pie',
    data: {
        labels: labelsProductos,
        datasets: [{
            data: dataProductos,
            backgroundColor: generateColors(labelsProductos.length),
            borderColor: '#fff',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true
    }
});

// Función para generar colores aleatorios
function getRandomColor() {
    const r = Math.floor(Math.random() * 255);
    const g = Math.floor(Math.random() * 255);
    const b = Math.floor(Math.random() * 255);
    return `rgba(${r}, ${g}, ${b}, 0.6)`;
}

// Función para generar múltiples colores
function generateColors(num) {
    const colors = [];
    for(let i = 0; i < num; i++) {
        colors.push(getRandomColor());
    }
    return colors;
}