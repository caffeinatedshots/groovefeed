function showonlyone(thechosenone) {
	$('.page').each(function(index) {
		if ($(this).attr("id") == thechosenone) {
			$(this).show();
			}
		else {
			$(this).hide();
			 }
	});
}