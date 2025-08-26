+function ($) { "use strict";

$(function(){

		var csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

		var base_url = $("#eco_base_url").val();

		$('.datatable:not(".someClass")').each(function() {

		var oTable = $(this).dataTable({
		"bProcessing": false,
		"sDom": "<'row'<'col-sm-6'l><'col-sm-6'f>r>t<'row'<'col-sm-6'i><'col-sm-6'p>>",
		"sPaginationType": "full_numbers",
		"language": {
			"url": base_url + "js/datatables/lang/French.json"
		},
		"lengthMenu": [[10, 25, 50, 100, 500, 1000], [10, 25, 50, 100, 500, 1000]],
		"bFilter" : true,
		"bLengthChange": true,
		"order": [[ 1, "desc" ]],
		});

		});

		$('#crtlBoxRecherche').click(function(){
			$('#boxRecherche').toggle();
		});

		//Added on 25-10-2024
		$('.btnSupprimerVoiture').click(function(){

			var voiture_id = $(this).attr('data-voiture_id');

			noty({
				dismissQueue: false,
				force: true,
				layout:'center',
				modal: true,
				theme: 'defaultTheme',
				text:"Voulez-vous vraiment supprimer cette voiture ?",
				type: 'warning',
				buttons: [
					{addClass: 'btn btn-success ', text: 'Oui', onClick: function($noty) {
							$noty.close();

						$.ajax({
							headers:{'X-CSRF-TOKEN': csrf_token},
							type:'post',
							url: base_url.trim() + 'supprimer_voiture',
							data: {voiture_id:voiture_id},
							success: function(data){

								if(data == 1){
									notification("Voiture supprimée avec succès !","success");
								}else{
									notification('Erreur lors de la suppression !',"warning");
								}

							},
							error: function(){
								notification("Erreur lors du traitement !","error");
							}
						});

						}},
						{addClass: 'btn btn-danger ', text: 'Non', onClick: function($noty) {
							$noty.close();
						}}]
			});


		});

		//Added on 28-10-2024
		$('.SupprimerEquipementVoiture').click(function(){

			var equipement_voiture_id = $(this).attr('data-equipement_voiture_id');

			noty({
				dismissQueue: false,
				force: true,
				layout:'center',
				modal: true,
				theme: 'defaultTheme',
				text:"Voulez-vous vraiment supprimer cet équipement de bord ?",
				type: 'warning',
				buttons: [
					{addClass: 'btn btn-success ', text: 'Oui', onClick: function($noty) {
							$noty.close();

						$.ajax({
							headers:{'X-CSRF-TOKEN': csrf_token},
							type:'post',
							url: base_url.trim() + 'supprimer_equipement_voiture',
							data: {equipement_voiture_id:equipement_voiture_id},
							success: function(data){

								if(data == 1){
									notification("Equipement de bord supprimé avec succès !","success");
								}else{
									notification('Erreur lors de la suppression !',"warning");
								}

							},
							error: function(){
								notification("Erreur lors du traitement !","error");
							}
						});

						}},
						{addClass: 'btn btn-danger ', text: 'Non', onClick: function($noty) {
							$noty.close();
						}}]
			});


		});

		//Added on 30-10-2024
		$('.btnSupprimerDiagnostique').click(function(){

			var diagnostique_id = $(this).attr('data-diagnostique_id');

			noty({
				dismissQueue: false,
				force: true,
				layout:'center',
				modal: true,
				theme: 'defaultTheme',
				text:"Voulez-vous vraiment supprimer ce diagnostique ?",
				type: 'warning',
				buttons: [
					{addClass: 'btn btn-success ', text: 'Oui', onClick: function($noty) {
							$noty.close();

						$.ajax({
							headers:{'X-CSRF-TOKEN': csrf_token},
							type:'post',
							url: base_url.trim() + 'supprimer_diagnostique_voiture',
							data: {diagnostique_id:diagnostique_id},
							success: function(data){

								if(data == 1){
									notification("Diagnostique supprimé avec succès !","success");
								}else{
									notification('Erreur lors de la suppression !',"warning");
								}

							},
							error: function(){
								notification("Erreur lors du traitement !","error");
							}
						});

						}},
						{addClass: 'btn btn-danger ', text: 'Non', onClick: function($noty) {
							$noty.close();
						}}]
			});


		});

		//Added on 30-10-2024
		$('.btnValiderDiagnostique').click(function(){

			var diagnostique_id = $(this).attr('data-diagnostique_id');

			noty({
				dismissQueue: false,
				force: true,
				layout:'center',
				modal: true,
				theme: 'defaultTheme',
				text:"Voulez-vous vraiment valider ce diagnostique ?",
				type: 'warning',
				buttons: [
					{addClass: 'btn btn-success ', text: 'Oui', onClick: function($noty) {
							$noty.close();

						$.ajax({
							headers:{'X-CSRF-TOKEN': csrf_token},
							type:'post',
							url: base_url.trim() + 'valider_diagnostique_voiture',
							data: {diagnostique_id:diagnostique_id},
							success: function(data){

								if(data == 1){
									notification("Diagnostique validé et sa facture générée avec succès !","success");
								}else{
									notification('Erreur lors de la validation !',"warning");
								}

							},
							error: function(){
								notification("Erreur lors du traitement !","error");
							}
						});

						}},
						{addClass: 'btn btn-danger ', text: 'Non', onClick: function($noty) {
							$noty.close();
						}}]
			});


		});

		//Added on 30-10-2024
		$('.btnValiderFactureDiagnostique').click(function(){

			var fac_diagnostique_id = $(this).attr('data-fac_diagnostique_id');

			noty({
				dismissQueue: false,
				force: true,
				layout:'center',
				modal: true,
				theme: 'defaultTheme',
				text:"Voulez-vous vraiment valider cette facture ?",
				type: 'warning',
				buttons: [
					{addClass: 'btn btn-success ', text: 'Oui', onClick: function($noty) {
							$noty.close();

						$.ajax({
							headers:{'X-CSRF-TOKEN': csrf_token},
							type:'post',
							url: base_url.trim() + 'valider_facture_diagnostique_voiture',
							data: {fac_diagnostique_id:fac_diagnostique_id},
							success: function(data){

								if(data == 1){
									notification("Facture validée et la ligne de réparation créée avec succès !","success");
								}else{
									notification('Erreur lors de la validation !',"warning");
								}

							},
							error: function(){
								notification("Erreur lors du traitement !","error");
							}
						});

						}},
						{addClass: 'btn btn-danger ', text: 'Non', onClick: function($noty) {
							$noty.close();
						}}]
			});


		});

		//NOTY
		function notification(text,type,callback){

			noty({
				dismissQueue: false,
				force: true,
				layout:'center',
				modal: true,
				theme: 'defaultTheme',
				text:text,
				type: type,
				buttons: [{addClass: 'btn btn-information ', text: 'OK', onClick: function($noty) {
					location.href = "";
					$noty.close();

				}}]
			});
		}

		//Appliquer les masques de saisie
		$('select').select2({
			placeholder: "Choisir",
			allowClear: true
		});


	});
}(window.jQuery);
