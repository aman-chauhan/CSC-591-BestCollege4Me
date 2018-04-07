var width = $( window ).width() * 0.50,
	height = $( window ).height() * 0.75;

var svg = d3.select( "#graph_col" ).append( "svg" )
	.attr( "width", width )
	.attr( "height", height );

var projection = d3.geoAlbersUsa().translate( [width/2, height/2] );
var path = d3.geoPath()
	.projection( projection );

var tool = d3.select( "body" )
	.append( "div" )
	.attr( "class", "tooltip" )
	.style( "opacity", 0 );

d3.json( "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json", function( error, us ) {

	svg.selectAll( "path" )
		.data( us.features )
		.enter()
			.append( "path" )
			.attr( "d", path )
			.style( "stroke", "#000000" )
			.style( "stroke-width", "1" )
			.style( "fill", "rgba( 255, 255, 255, 0.4 )" )
			.attr( "id", function( d ) { return d.properties.name; } );

	d3.json( "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.main_campus=1&school.operating=1&school.religious_affiliation=71&school.degrees_awarded.predominant=3&_fields=school.name,location.lat,location.lon,&api_key=MakhOqpDrxhHeP2ZdhQdgEOMApvxyGEW59VEfzYA&per_page=100", function( error, univ ) {

		var g = svg.append( "g" );

		g.selectAll( "circle" )
	  		.data( univ.results )
	  		.enter()
	  			.append( "circle" )
	  			.attr( "class", "circle" )
	  			.attr( "cx", function( d ) { return projection( [d['location.lon'], d['location.lat']] )[0]; } )
	  			.attr( "cy", function( d ) { return projection( [d['location.lon'], d['location.lat']] )[1]; } )
	  			.attr( "r", 6 )
	  			.style( "fill", "#CC0000" )
	  			.style( "opacity", 0.75 )
	  			.style( "stroke", "#fff" )
	  			.style( "stroke-width", 0 )
	  			.on( "mouseover", function( d ) {
	  				d3.select( this )
	  					.transition()
	  					.duration( 250 )
	  					.attr( "r", 9 )
	  					.style( "stroke-width", 4 );
	  				tool.transition()
	  					.duration( 250 )
	  					.style( "opacity", 0.85 );
	  				tool.html( d['school.name'] )
	  					.style( "left", ( d3.event.pageX ) + "px" )
	  					.style( "top", ( d3.event.pageY - 12 * 2 ) + "px" )
		  		} )
		  		.on( "mouseout", function( d ) {
		  			d3.select( this )
	  					.transition()
	  					.duration( 250 )
	  					.attr( "r", 6 )
	  					.style( "stroke-width", 0 );
		  			tool.transition()
		  				.duration( 250 )
		  				.style( "opacity", 0 );
		  		} );
	} );
} );