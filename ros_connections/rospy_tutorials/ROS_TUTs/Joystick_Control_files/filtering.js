

 
 
 
 	$(document).ready(function(){
		
				
			//defines the default category 
			$('#content ul li:not(.tabzero)').hide();


			//when a link in the filters div is clicked...
			$('#filters a').click(function(e){

			//prevent the default behaviour of the link
			e.preventDefault();

			//get the id of the clicked link(which is equal to classes of our content
			var filter = $(this).attr('id');

			//show all the list items(this is needed to get the hidden ones shown)
			$('#content ul li').show();

			/*using the :not attribute and the filter class in it we are selecting
			only the list items that don't have that class and hide them '*/
			$('#content ul li:not(.' + filter + ')').hide();

		});

	});
