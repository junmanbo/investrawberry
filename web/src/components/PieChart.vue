<template>
    <div ref="chart"></div>
</template>

<script>
import { onMounted, ref, watch } from 'vue';
import * as d3 from 'd3';

export default {
    name: 'PieChart',
    props: {
        data: {
            type: Array,
            required: true,
        },
        size: {
            type: Number,
            default: 450,
        },
    },
    setup(props) {
        const chart = ref(null);
        let svg, pie, arc;

        // Set the dimensions and margins of the graph
        const margin = 40;

        onMounted(() => {
            // The radius of the pie chart is half the smallest side
            const radius = props.size / 2 - margin;

            // Append SVG element
            svg = d3.select(chart.value)
                .append('svg')
                .attr('width', props.size)
                .attr('height', props.size)
                .append('g')
                .attr('transform', 'translate(' + props.size / 2 + ',' + props.size / 2 + ')');

            // Create pie generator
            pie = d3.pie().value(d => d.value);

            // Create arc generator
            arc = d3.arc().innerRadius(0).outerRadius(radius);
        });

        watch(() => props.data, (newData) => {
            const data = newData;

            // Update the pie chart
            svg.selectAll('path')
                .data(pie(data))
                .join(
                    (enter) =>
                        enter
                            .append('path')
                            .attr('d', arc)
                            .attr('fill', (d) => d.data.color),
                    (update) =>
                        update.attr('d', arc),
                    (exit) => exit.remove()
                );
        });
        return { chart };
    },
};
</script>

