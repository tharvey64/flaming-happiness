$(document).ready(function(){    
    $('#searchTwitter').on('submit', function(event){
        event.preventDefault();
        $.post($(this).attr('action'),
            {'search': ($('#search')).val(), csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value, 'type' :$('[name=filter]').val() },
            function(data) {
                var dataset = []
                var dates = data['dates'] 
                var favorites = data['favorites']
                var feelings = data['feelings']
                for (i=0; i < dates.length; i++) {
                    if (feelings[i]['feeling']['docSentiment'] != undefined){
                        dataset.push([dates[i]['date'], favorites[i]['favorite'], feelings[i]['feeling']['docSentiment']['score']])
                    }
                    else{
                        continue
                    }
                } 
            var padding = 30;
            var graphHeight = parseInt($("#graph").css('height'));
            var h = graphHeight
            var graphWidth = parseInt($("#graph").css('width'));
            var w = graphWidth; 
            var parseDate = d3.time.format("%a %B %e %X %Z %Y").parse; 

            var yScale = d3.scale.linear()
                .domain([0, d3.max(dataset,function(d){return d[1]})])
                .range([h - padding, padding]);    

            var xScale = d3.time.scale()
                .domain(d3.extent(dataset, function(d){
                    return parseDate(d[0]);
                }))
                .range([padding, w - padding]);

            var svg = d3.select("#graph")
                        .append("svg")
                        .attr("width", w)
                        .attr("height", h)  
            svg.selectAll("circle")
                .data(dataset)
                .enter()
                .append("circle")
                .attr("cx", function(d) {
                    return xScale(parseDate(d[0]));
                })
                .attr("cy", function(d){
                    console.log(h)
                    return yScale(d[1])
                })
                .attr("r", function(d) {
                    return 5;
                })
                .attr("fill", function(d) {
                    return d3.rgb((d[2] * -255),(d[2] * 255),0);
                });
        //         var template = $('#sentimentTemplate').html();
        //         Mustache.parse(template);
        //         var info = Mustache.render(template, data);
        //         $('#postedSearch').html(info);
        //         var template = $('#tweetTemplate').html();
        //         Mustache.parse(template);
        //         var info = Mustache.render(template, data);
        //         $('#postedTweets').html(info); 
        //         var template = $('#hashTemplate').html();
        //         Mustache.parse(template);
        //         var info = Mustache.render(template, data);
        //         $('#postedHashes').html(info);                                 
            }
        )
    
    })
});
