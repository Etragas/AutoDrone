
jQuery(document).ready(function(){
    jQuery("#donate_popup_close").click(function(){
	jQuery("#donate_popup").css('display', 'none');
    	jQuery.ajax('/donate_close');
      });
  });
