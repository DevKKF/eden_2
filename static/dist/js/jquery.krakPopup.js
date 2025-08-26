(function($) {
	/*Author: Armand Kouassi (krak225@gmail.com | +22504783689) */
	
	// définition du plugin jQuery
	$.fn.krakPopup = function(params) {
		
		//Paramètres par défaut
		var defaults = {
			width: 430, 
			height: 50,
			contentMinHeight: 140,
			title:'Ma boite de dialogue',
			content:'<div class="default-content">Le corps de la boite de dialogue</div>',
			url:'',
			onOutClickClose:false,
			closeButton:false,
			submitButton:true,
			customButton:{show:true,text:'Boutton',clickFn:function(){alert('A Click on customButton')}},
			onFinish:function(){
				// $('#krakPopupInfoBox').html('Popup affiché avec succès');
				// alert('Popup affiché avec succès');
			},
			//
			positionLeft:'center',
			positionTop:'center'
		};
		
		// Fusionner les paramètres par défaut et ceux de l'utilisateur
		params = $.extend(defaults, params);
				
		
		// Traverser tous les nœuds.
		this.each(function(){
			// Exprimer un nœud seul en objet jQuery
			var element = $(this);
			element.hide();
			
			if(element.attr('data-title')!=null){
				params.title = element.attr('data-title');
			}
			
			
			// Création de l'overlay
			var overlay = $('<div class="krakPopup_overlay" style="display:none;"></div>');
			$('body').append(overlay);
			$('.krakPopup_overlay').fadeIn("slow");
			
			//Création du popup
			var dialogBox = ('<div id="dialogBox" class="dialogBox krakPopup"></div>');
			
			//Insertion du popup dans le body
			$('body').append(dialogBox);
			
			//Appliquer des styles au popup
			$('#dialogBox').css({
				display:'block',
				width:params.width,
				'min-height':params.height
			});
			
			
			//Ajout de propriétés Jquery UI
			$('#dialogBox').draggable();
			// $('#dialogBox').resizable();
			// $('#dialogBox').selectable();
			
			//Positionnement sur l'écran
			if(params.positionTop!='center'){
				// alert('sdsd');
				setTimeout(
					function(){
						$("#dialogBox").animate(
							{
								'top':params.positionTop,
								'left':params.positionLeft,
								margin:'auto'
							},
							function(){
								
							}
						);
					},
					500);
			}else{
				var body_width = $('body').width();
				var leftPos = (body_width / 2) - ($("#dialogBox").width() /2);
				$("#dialogBox").animate(
					{
						'top':'10%',
						'position':'absolute',
						'left':leftPos
					},
					function(){
						// alert();
						// $("#dialogBox").css({top:'50%',position:'absolute','left':'33%'});
					}
				);
				

			}
			
			
			//Adapter à l'écran
			var body_width = $('body').width();
			var leftPos = (body_width / 2) - ($("#dialogBox").width() /2);
			$("#dialogBox").css({'left':leftPos,'max-width':body_width});
			if($("#dialogBox").width()==body_width){
				$("#dialogBox").css({'left':0});
			}
			
			//CENTRER LA FENETRE LORS DU ZOOM 
			$(window).resize(function(){
				var body_width = $('body').width();
				var leftPos = (body_width / 2) - ($("#dialogBox").width() /2);
				$("#dialogBox").css({'left':leftPos,'max-width':body_width});
				if($("#dialogBox").width()==body_width){
					$("#dialogBox").css({'left':0});
				}
			});
			
			//Création de l'entête du popup
			var header = ('<div id="modal-header"><h2 class="modal-title" style="padding:10px 0px;height:43px;border:0px solid red;"><span id="modal-title">'+params.title+'</span><span class="btn_close" id="btn_close" title="Fermer">x</span></h2></div>');
			$('#dialogBox').append(header);
			
			//Création du contenu du popup
			// var content = ('<div id="modal-content"><div id="content-wrapper">'+ params.content +'</div></div>');
			var content = ('<div id="modal-content"><div id="krakPopupInfoBox" style="min-height:25px;"></div><div id="content-wrapper"></div></div>');
			$('#dialogBox').append(content);
			
			//Charger le contenu
			if(params.url!=''){
				$('#krakPopupInfoBox').html('Chargement en cours...');
				$('#content-wrapper').load(params.url,function(){
					$('#krakPopupInfoBox').html('');
				});
			}else{
				params.content = element.html();
				$('#content-wrapper').html(params.content);
				// ALERT('dd');
			}
			
			
			//Création du pied de page du popup
			var footer = ('<div id="modal-footer"></div>');
			$('#dialogBox').append(footer);
			
			var close_button = '<input type="button" class="btn btn_close" value="Fermer"/>';
			var submit_button = '<input type="button" class="btn btn_close" value="Valider"/>';
			var custom_button = '<input type="button" class="btn customButton" value="'+params.customButton.text+'" id="customButton"/>';
			if(params.closeButton){
				$('#modal-footer').append(close_button);
			}
			if(params.submitButton){
				$('#modal-footer').append(submit_button);
			}
			if(params.customButton.show){
				// alert(params.customButton.text);
				$('#modal-footer').append(custom_button);
			}
			
			$('#customButton').click(function(){
				// alert(params.customButton.clickFn);
				params.customButton.clickFn();
			});
		
			//Ajout des effets
			$('#modal-content > #content-wrapper').hide();
			setTimeout(
				function(){
					$("#modal-content").animate(
						{'min-height':params.contentMinHeight},
						function(){
							
							$('#modal-content > #content-wrapper').fadeIn("slow", function(){
								
								
								//Exécuter mon callback onFinish
								params.onFinish();
								
							});
							
							
						}
					);
				},
				500);
			
			
			// Dans le cas ou une Callback a été passé on l'exécute.
			/* if (typeof params.onFinish === "function") {
				params.onFinish();
			}
			 */
			
			
			//Fonction de fermeture du popup
			function closePopup(){
				$('#dialogBox').fadeOut('slow',function(){
					$('#dialogBox').html('');
					$('#dialogBox').remove();
					$('.krakPopup_overlay').fadeOut("slow");
					$('.krakPopup_overlay').remove();
					$('.krakPopup_overlay').html("");
				});
			}
			
			//Boutton Fermer
			$('.btn_close').click(function(){
				closePopup();
			});
			
			//Click en dehors du popup pour fermer 
			if(params.onOutClickClose){
				$('.krakPopup_overlay').click(function(){
					closePopup();
				});
			}
			
			
			
		});
		
		// Permettre le chaînage par jQuery
		return this;
	};
})(jQuery);