function map_builder( ret_data ) {
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

		var g = svg.append( "g" );

		g.selectAll( "circle" )
		  	.data( ret_data.results )
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
		  				.style( "top", ( d3.event.pageY - 18 * 2 ) + "px" )
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

		g.selectAll( "text" )
			.data( [{ lat : 35.097079, lon : -80.773301 }] )
			.enter()
			.append( "text" )
				.attr( "x", function( d ) { return projection( [d.lon, d.lat] )[0]; } )
			  	.attr( "y", function( d ) { return projection( [d.lon, d.lat] )[1]; } )
				.attr( 'font-family', 'FontAwesome' )
				.attr( 'font-size', '12px' )
				.attr( 'fill', 'yellow' )
				.text( '\uf015' )
				.on( "mouseover", function( d ) {
		  			d3.select( this )
		  				.transition()
		  				.duration( 250 )
		  				.attr( 'font-size', '18px' )
		  			tool.transition()
		  				.duration( 250 )
		  				.style( "opacity", 0.85 );
		  			tool.html( 'You are here' )
		  				.style( "left", ( d3.event.pageX ) + "px" )
		  				.style( "top", ( d3.event.pageY - 18 * 2 ) + "px" )
			  	} )
			  	.on( "mouseout", function( d ) {
			  		d3.select( this )
		  				.transition()
		  				.duration( 250 )
		  				.attr( 'font-size', '12px' )
			  		tool.transition()
			  			.duration( 250 )
			  			.style( "opacity", 0 );
			  	} );
	} );
}