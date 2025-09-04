$(document).ready(function () {
    function getCSRFToken() {
        return $("input[name=csrfmiddlewaretoken]").val();
    }

    if (!Object.keys) {
      Object.keys = (function () {
        'use strict';
        var hasOwnProperty = Object.prototype.hasOwnProperty,
            hasDontEnumBug = !({ toString: null }).propertyIsEnumerable('toString'),
            dontEnums = [
              'toString',
              'toLocaleString',
              'valueOf',
              'hasOwnProperty',
              'isPrototypeOf',
              'propertyIsEnumerable',
              'constructor'
            ],
            dontEnumsLength = dontEnums.length;

        return function (obj) {
          if (typeof obj !== 'object' && (typeof obj !== 'function' || obj === null)) {
            throw new TypeError('Object.keys called on non-object');
          }

          var result = [], prop, i;

          for (prop in obj) {
            if (hasOwnProperty.call(obj, prop)) {
              result.push(prop);
            }
          }

          if (hasDontEnumBug) {
            for (i = 0; i < dontEnumsLength; i++) {
              if (hasOwnProperty.call(obj, dontEnums[i])) {
                result.push(dontEnums[i]);
              }
            }
          }
          return result;
        };
      }());
    }

    var my_noty;
    function notifySuccess(message, fnCallback) {
        my_noty = noty({
            text: message,
            type: 'success',
            dismissQueue: true,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'btn btn-primary', text: 'OK', onClick: function ($noty) {

                        if (typeof fnCallback === 'function') fnCallback();

                        $noty.close();
                    }
                }
            ]
        });
    }

    function notifyWarning(message, fnCallback) {
        if (my_noty) {
            my_noty.close();
        }

        my_noty = noty({
            text: message,
            type: 'warning',
            dismissQueue: true,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'btn btn-primary', text: 'OK', onClick: function ($noty) {

                        if (typeof fnCallback === 'function') fnCallback();

                        $noty.close();
                    }
                }
            ]
        });

    }

    function notifyError(message, fnCallback) {
        my_noty = noty({
            text: message,
            type: 'error',
            dismissQueue: true,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'btn btn-primary', text: 'OK', onClick: function ($noty) {

                        if (typeof fnCallback === 'function') fnCallback();

                        $noty.close();
                    }
                }
            ]
        });
    }

    function notifyInfo(message, fnCallback) {
        if (my_noty) {
            my_noty.close();
        }

        my_noty = noty({
            text: message,
            type: 'info',
            dismissQueue: true,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'btn btn-info', text: 'OK', onClick: function ($noty) {

                        if (typeof fnCallback === 'function') fnCallback();

                        $noty.close();
                    }
                }
            ]
        });

    }

    // Using jQuery
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie != '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    // Fonction pour réinitialiser tous les champs d'un formulaire
    function resetFields(formSelector) {
        let $form = $(formSelector);

        if ($form.length) {
            // Réinitialiser tous les champs du formulaire
            $form[0].reset();

            // Supprimer toutes les classes d'erreur
            $form.find('.form-group').removeClass('has-error');
            $form.find('input, select, textarea').removeClass('is-invalid');

            // Masquer tous les messages d'erreur
            $form.find('.error-text').hide().text('');
            $form.find('[class$="_error"]').hide().text('');

            // Masquer les alertes dans le modal
            $form.closest('.modal').find('.alert').addClass('hidden').removeClass('alert-warning alert-success');
        }
    }

    // Fonction pour capitaliser la première lettre
    function ucfirst(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    /* TODO SESSION DE FORMATION DEBUT */
    $(document).on('click', "#btn_save_session", function () {
        let formulaire = $('#form_add_session');
        let href = formulaire.attr('action');

        // Déclaration de formData au niveau de la portée de la fonction
        let formData = new FormData();

        // Validation manuelle des champs requis
        let nom = $('#nom').val().trim();
        let date_debut = $('#date_debut').val().trim();
        let date_fin = $('#date_fin').val().trim();

        // Variable pour vérifier si tout est valide
        let is_valid = true;

        // Masquer toutes les erreurs et enlever les classes d'erreur
        $('.form-group').removeClass('has-error');
        $('.error-text').hide().text('');

        if (nom === '') {
            $('#nom').closest('.form-group').addClass('has-error');
            is_valid = false;
        }
        if (date_debut === '') {
            $('#date_debut').closest('.form-group').addClass('has-error');
            is_valid = false;
        }
        if (date_fin === '') {
            $('#date_fin').closest('.form-group').addClass('has-error');
            is_valid = false;
        }

        if (is_valid) {
            let n = noty({
                text: 'Voulez-vous vraiment enregistrer cette session de formation ?',
                type: 'warning',
                dismissQueue: true,
                layout: 'center',
                theme: 'defaultTheme',
                buttons: [
                    {
                        addClass: 'btn btn-primary', text: 'Valider', onClick: function ($noty) {
                            $noty.close();

                            let data_serialized = formulaire.serialize();
                            $.each(data_serialized.split('&'), function (index, elem) {
                                let vals = elem.split('=');
                                let key = vals[0];
                                let valeur = decodeURIComponent(vals[1].replace(/\+/g, '  '));
                                formData.append(key, valeur);
                            });

                            $.ajax({
                                type: 'post',
                                url: href,
                                data: formData,
                                processData: false,
                                contentType: false,
                                success: function (response) {
                                    if (response.statut == 1) {
                                        resetFields('#' + formulaire.attr('id'));
                                        notifySuccess(response.message, function () {
                                            location.reload();
                                        });
                                    }
                                    if (response.statut == 0) {
                                        let errors_list_to_display = '';

                                        for (let field in response.errors) {
                                            let messages = response.errors[field].join('<br/>');
                                            errors_list_to_display += `<br/><i class="fa fa-arrow-circle-right"></i> ${messages}`;

                                            // Mettre en rouge le champ concerné
                                            $('#' + field).addClass('is-invalid');
                                        }

                                        // Afficher les erreurs dans l'alerte
                                        $('#modal-add_session .alert .message').html(errors_list_to_display);
                                        $('#modal-add_session .alert').removeClass('hidden').show();
                                        console.log('errors_list_to_display : ', errors_list_to_display);
                                    }
                                },
                                error: function (request, status, error) {
                                    notifyWarning("Erreur lors de l'enregistrement");
                                }
                            });
                        }
                    },
                    {
                        addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                            $noty.close();
                        }
                    }
                ]
            });
        } else {
            notifyWarning('Veuillez renseigner correctement le formulaire');
        }
    });

    $(document).on('click', '.btn_modifier_session', function () {
        let model_name = $(this).attr('data-model_name');
        let modal_title = $(this).attr('data-modal_title');
        let href = $(this).attr('data-href');

        $('#eden_std_dialog_box').load(href, function () {

            $('#modal-modification_session').attr('data-backdrop', 'static').attr('data-keyboard', false);

            $('#modal-modification_session').find('#btn_valider').attr({ 'data-model_name': model_name, 'data-href': href });
            $('#modal-modification_session').find('.modal-dialog');

            //
            $('#modal-modification_session').modal();

            //gestion du clique sur valider les modifications
            $("#btn_save_modification_session").on('click', function () {
                let formulaire = $('#form_update_session');
                let href = formulaire.attr('action');

                // Déclaration de formData au niveau de la portée de la fonction
                let formData = new FormData();

                // Validation manuelle des champs requis (AJOUTÉ)
                let nom = $('#edit_nom').val();
                let date_debut = $('#edit_date_debut').val();
                let date_fin = $('#edit_date_fin').val();

                // Variable pour vérifier si tout est valide
                let is_valid = true;

                // Masquer toutes les erreurs et enlever les classes d'erreur (AJOUTÉ)
                $('.form-group').removeClass('has-error');
                $('.error-text').hide().text('');

                // Validations des champs requis (AJOUTÉ)
                if (nom === '') {
                    $('#edit_nom').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }
                if (date_debut === '') {
                    $('#edit_date_debut').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }
                if (date_fin === '') {
                    $('#edit_date_fin').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }

                if (is_valid) {
                    let n = noty({
                        text: 'Voulez-vous vraiment modifier cette session de formation ?',
                        type: 'warning',
                        dismissQueue: true,
                        layout: 'center',
                        theme: 'defaultTheme',
                        buttons: [
                            {
                                addClass: 'btn btn-primary', text: 'Valider', onClick: function ($noty) {
                                    $noty.close();

                                    let data_serialized = formulaire.serialize();
                                    $.each(data_serialized.split('&'), function (index, elem) {
                                        let vals = elem.split('=');
                                        let key = vals[0];
                                        let valeur = decodeURIComponent(vals[1].replace(/\+/g, '  '));
                                        formData.append(key, valeur);
                                    });

                                    $.ajax({
                                        type: 'post',
                                        url: href,
                                        data: formData,
                                        processData: false,
                                        contentType: false,
                                        success: function (response) {
                                            if (response.statut == 1) {
                                                resetFields('#' + formulaire.attr('id'));
                                                notifySuccess(response.message, function () {
                                                    location.reload();
                                                });
                                            }
                                            if (response.statut == 0) {
                                                let errors_list_to_display = '';

                                                for (let field in response.errors) {
                                                    let messages = response.errors[field].join('<br/>');
                                                    errors_list_to_display += `<br/><i class="fa fa-arrow-circle-right"></i> ${messages}`;

                                                    // Mettre en rouge le champ concerné
                                                    $('#' + field).addClass('is-invalid');
                                                }

                                                // Afficher les erreurs dans l'alerte (CORRIGÉ: référence au bon modal)
                                                $('#modal-modification_session .alert .message').html(errors_list_to_display);
                                                $('#modal-modification_session .alert').removeClass('hidden').show();
                                                console.log('errors_list_to_display : ', errors_list_to_display);
                                            }
                                        },
                                        error: function (request, status, error) {
                                            notifyWarning("Erreur lors de l'enregistrement");
                                        }
                                    });
                                }
                            },
                            {
                                addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                                    $noty.close();
                                }
                            }
                        ]
                    });
                } else {
                    notifyWarning('Veuillez renseigner correctement le formulaire');
                }
            });

        });
    });

    $(document).on('click', '.btn_supprimer_session', function () {
        let session_id = $(this).data('session_id');

        let n = noty({
            text: 'Voulez-vous vraiment supprimer cette session de formation ?',
            type: 'warning',
            dismissQueue: true,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'btn btn-primary', text: 'Supprimer', onClick: function ($noty) {
                        $noty.close();

                        //effectuer la suppression
                        $.ajax({
                            url: '/dashboard/sessions/session/delete',
                            type: 'post',
                            data: { session_id: session_id },
                            headers: { 'X-CSRFToken': getCookie('csrftoken') },
                            success: function (response) {
                                if (response.statut == 1) {
                                    notifySuccess(response.message, function () {
                                        location.reload();
                                    });
                                }
                            },
                            error: function () {
                                notifyWarning('Erreur lors de la suppression');
                            }
                        });

                    }
                },
                {
                    addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                        //annuler la suppression
                        $noty.close();
                    }
                }
            ]
        });
    });
    /* TODO SESSION DE FORMATION FIN */

    /* TODO CERTIFICATS DE LA SESSION DE FORMATION DEBUT */
    $(document).on('click', "#btn_save_certificat", function () {
        let formulaire = $('#form_add_certificat');
        let href = formulaire.attr('action');

        // Déclaration de formData au niveau de la portée de la fonction
        let formData = new FormData();

        // Validation manuelle des champs requis
        let nombre = $('#nombre').val().trim();
        let date_debut_validite = $('#date_debut_validite').val().trim();
        let date_fin_validite = $('#date_fin_validite').val().trim();

        // Variable pour vérifier si tout est valide
        let is_valid = true;

        // Masquer toutes les erreurs et enlever les classes d'erreur
        $('.form-group').removeClass('has-error');
        $('.error-text').hide().text('');

        if (nombre === '') {
            $('#nombre').closest('.form-group').addClass('has-error');
            is_valid = false;
        } else {
            // Supprimer les espaces pour obtenir un nombre valide
            let nombre_clean = parseInt(nombre.replace(/\s/g, ''));
            if (isNaN(nombre_clean) || nombre_clean <= 0) {
                $('#nombre').closest('.form-group').addClass('has-error');
                notifyWarning('Veuillez saisir un nombre valide supérieur à 0.');
                is_valid = false;
            } else if (nombre_clean > 300) {
                $('#nombre').val(''); // Vider le champ
                $('#nombre').closest('.form-group').addClass('has-error');
                notifyWarning('Le nombre saisi ne peut pas dépasser 300.');
                is_valid = false;
            }
        }
        if (date_debut_validite === '') {
            $('#date_debut_validite').closest('.form-group').addClass('has-error');
            is_valid = false;
        }
        if (date_fin_validite === '') {
            $('#date_fin_validite').closest('.form-group').addClass('has-error');
            is_valid = false;
        }

        if (is_valid) {
            let n = noty({
                text: 'Voulez-vous vraiment enregistrer le certificat de la session de formation ?',
                type: 'warning',
                dismissQueue: true,
                layout: 'center',
                theme: 'defaultTheme',
                buttons: [
                    {
                        addClass: 'btn btn-primary', text: 'Valider', onClick: function ($noty) {
                            $noty.close();

                            let data_serialized = formulaire.serialize();
                            $.each(data_serialized.split('&'), function (index, elem) {
                                let vals = elem.split('=');
                                let key = vals[0];
                                let valeur = decodeURIComponent(vals[1].replace(/\+/g, '  '));
                                formData.append(key, valeur);
                            });

                            $.ajax({
                                type: 'post',
                                url: href,
                                data: formData,
                                processData: false,
                                contentType: false,
                                success: function (response) {
                                    if (response.statut == 1) {
                                        resetFields('#' + formulaire.attr('id'));
                                        notifySuccess(response.message, function () {
                                            location.reload();
                                        });
                                    }
                                    if (response.statut == 0) {
                                        let errors_list_to_display = '';

                                        for (let field in response.errors) {
                                            let messages = response.errors[field].join('<br/>');
                                            errors_list_to_display += `<br/><i class="fa fa-arrow-circle-right"></i> ${messages}`;

                                            // Mettre en rouge le champ concerné
                                            $('#' + field).addClass('is-invalid');
                                        }

                                        // Afficher les erreurs dans l'alerte
                                        $('#modal-add_certificat .alert .message').html(errors_list_to_display);
                                        $('#modal-add_certificat .alert').removeClass('hidden').show();
                                        console.log('errors_list_to_display : ', errors_list_to_display);
                                    }
                                },
                                error: function (request, status, error) {
                                    notifyWarning("Erreur lors de l'enregistrement");
                                }
                            });
                        }
                    },
                    {
                        addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                            $noty.close();
                        }
                    }
                ]
            });
        } else {
            notifyWarning('Veuillez renseigner correctement le formulaire');
        }
    });

    // Initialisation DataTable
    let table = $('#certificat_sessions_datatables').DataTable();

    $(document).on('click', '.btn_detail_certificat', function () {
        let model_name = $(this).attr('data-model_name');
        let modal_title = $(this).attr('data-modal_title');
        let href = $(this).attr('data-href');

        $('#eden_std_dialog_box').load(href, function () {

            $('#modal-detail_certificat').attr('data-backdrop', 'static').attr('data-keyboard', false);

            $('#modal-detail_certificat').find('#btn_valider').attr({ 'data-model_name': model_name, 'data-href': href });
            $('#modal-detail_certificat').find('.modal-dialog');

            //
            $('#modal-detail_certificat').modal();

        });
    });

    // Fonction qui active/désactive le bouton
    function updateButtonState() {
        let anyChecked = $('input[name="certificat_ids[]"]:checked').length > 0;
        if (anyChecked) {
            $('.btn_supprimer_certificats').removeClass('disabled');
        } else {
            $('.btn_supprimer_certificats').addClass('disabled');
        }
    }

    // Délégation pour "select all"
    $(document).on('change', '#certificat_id_all', function () {
        $('input[name="certificat_ids[]"]').prop('checked', this.checked);
        updateButtonState();
    });

    // Délégation pour chaque checkbox de ligne
    $(document).on('change', 'input[name="certificat_ids[]"]', function () {
        // Si tous sont cochés → cocher le "select all"
        $('#certificat_id_all').prop(
            'checked',
            $('input[name="certificat_ids[]"]').length === $('input[name="certificat_ids[]"]:checked').length
        );
        updateButtonState();
    });

    // Suppression (reste pareil que plus haut)
    $(document).on('click', '.btn_supprimer_certificats', function () {
        let formulaire = $('#form_delete_certificats');
        let href = formulaire.attr('action');

        if ($(this).hasClass('disabled')) return;

        let certificatsIds = $('input[name="certificat_ids[]"]:checked').map(function () {
            return $(this).val();
        }).get();

        if (certificatsIds.length === 0) {
            notifyWarning('Aucun certificat sélectionné.');
            return;
        }

        let n = noty({
            text: 'Voulez-vous vraiment supprimer les certificats sélectionnés ?',
            type: 'warning',
            dismissQueue: true,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'btn btn-primary', text: 'Valider', onClick: function ($noty) {
                        $noty.close();
                        $.ajax({
                            type: 'POST',
                            url: href,
                            data: {
                                certificats_ids: certificatsIds,
                                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                            },
                            success: function (response) {
                                if (response.statut == 1) {
                                    notifySuccess(response.message, function () {
                                        location.reload();
                                    });
                                } else {
                                    notifyWarning(response.message || 'Erreur lors de la suppression.');
                                }
                            },
                            error: function () {
                                notifyWarning('Erreur lors de la suppression.');
                            }
                        });
                    }
                },
                {
                    addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                        $noty.close();
                    }
                }
            ]
        });
    });

    // Initialisation
    updateButtonState();
    /* TODO CERTIFICATS DE LA SESSION DE FORMATION FIN */

    /* TODO COURS DE LA SESSION DE FORMATION DEBUT */
    //Gestion sélection type cour (vidéo, audio, texte)
    function manage_type_cours_change() {
        // Récupérer l'élément option sélectionné
        let selectedOption = $('#modal-add_cours #type_cours_id option:selected');

        // Récupérer la valeur de l'attribut data-type_cours_code
        let type_cours_id = selectedOption.data('type_cours_code');

        $('.if_cours_video').hide();
        $('.if_cours_audio').hide();
        $('.if_cours_texte').hide();

        switch (type_cours_id) {
            default:
            case 'VIDEOS':// Vidéo
                $('.if_cours_video').show();
                $('.if_cours_video input').attr('required', 'required');
                break;
            case 'AUDIOS':// Audio
                $('.if_cours_audio').show();
                $('.if_cours_audio input').attr('required', 'required');
                break;
            case 'TEXTES':// Texte
                $('.if_cours_texte').show();
                $('.if_cours_texte input').attr('required', 'required');
                break;
        }
    }

    manage_type_cours_change();
    $(document).on('change', "#modal-add_cours #type_cours_id", function () {
        manage_type_cours_change();
    });

    $(document).on('click', "#btn_save_cours", function () {
        let formulaire = $('#form_add_cours');
        let href = formulaire.attr('action');

        let formData = new FormData();

        // Validation manuelle des champs requis
        let titre = $('#titre').val().trim();
        let type_cours_id = $('#type_cours_id').val().trim();
        let cours_video = $('#cours_video').val().trim();
        let cours_audio = $('#cours_audio').val().trim();
        let cours_texte = $('#cours_texte').val().trim();

        let is_valid = true;

        $('.form-group').removeClass('has-error');
        $('.error-text').hide().text('');

        if (titre === '') {
            $('#titre').closest('.form-group').addClass('has-error');
            is_valid = false;
        }
        if (type_cours_id === '') {
            $('#type_cours_id').closest('.form-group').addClass('has-error');
            is_valid = false;
        }

        let selectedOption = $('#modal-add_cours #type_cours_id option:selected');
        let type_cours_code = selectedOption.data('type_cours_code');

        if (type_cours_code === "VIDEOS" && cours_video === '') {
            $('#cours_video').closest('.form-group').addClass('has-error');
            is_valid = false;
        }

        if (type_cours_code === "AUDIOS" && cours_audio === '') {
            $('#cours_audio').closest('.form-group').addClass('has-error');
            is_valid = false;
        }

        if (type_cours_code === "TEXTES" && cours_texte === '') {
            $('#cours_texte').closest('.form-group').addClass('has-error');
            is_valid = false;
        }

        // Récupérer le bon input file en fonction du type choisi
        let coursFichierInput = "";
        if (type_cours_code === "VIDEOS") coursFichierInput = $('#form_add_cours #cours_video');
        if (type_cours_code === "AUDIOS") coursFichierInput = $('#form_add_cours #cours_audio');
        if (type_cours_code === "TEXTES") coursFichierInput = $('#form_add_cours #cours_texte');

        let files = [];
        if (coursFichierInput.length > 0) {
            files = coursFichierInput[0].files;
        }

        if (is_valid) {
            let n = noty({
                text: 'Voulez-vous vraiment enregistrer ce cours de la session de formation ?',
                type: 'warning',
                dismissQueue: true,
                layout: 'center',
                theme: 'defaultTheme',
                buttons: [
                    {
                        addClass: 'btn btn-primary', text: 'Valider', onClick: function ($noty) {
                            $noty.close();

                            // Use serializeArray() which is more reliable
                            let form_data_array = formulaire.serializeArray();
                            $.each(form_data_array, function (index, obj) {
                                formData.append(obj.name, obj.value);
                            });

                            console.log('files : ', files);
                            // Ajout du fichier correctement
                            if (files.length > 0) {
                                formData.append(coursFichierInput.attr('name'), files[0]);
                            }

                            $.ajax({
                                type: 'post',
                                url: href,
                                data: formData,
                                processData: false,
                                contentType: false,
                                success: function (response) {
                                    if (response.statut == 1) {
                                        resetFields('#' + formulaire.attr('id'));
                                        notifySuccess(response.message, function () {
                                            location.reload();
                                        });
                                    }
                                    if (response.statut == 0) {
                                        let errors_list_to_display = '';

                                        for (let field in response.errors) {
                                            let messages = response.errors[field].join('<br/>');
                                            errors_list_to_display += `<br/><i class="fa fa-arrow-circle-right"></i> ${messages}`;
                                            $('#' + field).addClass('is-invalid');
                                        }

                                        $('#modal-add_cours .alert .message').html(errors_list_to_display);
                                        $('#modal-add_cours .alert').removeClass('hidden').show();
                                    }
                                },
                                error: function (request, status, error) {
                                    notifyWarning("Erreur lors de l'enregistrement");
                                }
                            });
                        }
                    },
                    {
                        addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                            $noty.close();
                        }
                    }
                ]
            });
        } else {
            notifyWarning('Veuillez renseigner correctement le formulaire');
        }
    });

    function manage_update_type_cours_change() {
        // Récupérer l'élément option sélectionné
        let selectedOption = $('#modal-modification_cours #edit_type_cours_id option:selected');

        // Récupérer la valeur de l'attribut data-type_cours_code
        let type_cours_id = selectedOption.data('type_cours_code');

        $('.if_cours_video').hide();
        $('.if_cours_audio').hide();
        $('.if_cours_texte').hide();

        switch (type_cours_id) {
            default:
            case 'VIDEOS':// Vidéo
                $('.if_cours_video').show();
                $('.if_cours_video input').attr('required', 'required');
                break;
            case 'AUDIOS':// Audio
                $('.if_cours_audio').show();
                $('.if_cours_audio input').attr('required', 'required');
                break;
            case 'TEXTES':// Texte
                $('.if_cours_texte').show();
                $('.if_cours_texte input').attr('required', 'required');
                break;
        }
    }

    manage_update_type_cours_change();
    $(document).on('change', "#modal-modification_cours #edit_type_cours_id", function () {
        manage_update_type_cours_change();
    });

    $(document).on('click', '.btn_modifier_cours', function () {
        let model_name = $(this).attr('data-model_name');
        let modal_title = $(this).attr('data-modal_title');
        let href = $(this).attr('data-href');

        $('#eden_std_dialog_box').load(href, function () {

            manage_update_type_cours_change()

            $('#modal-modification_cours').attr('data-backdrop', 'static').attr('data-keyboard', false);

            $('#modal-modification_cours').find('#btn_valider').attr({ 'data-model_name': model_name, 'data-href': href });
            $('#modal-modification_cours').find('.modal-dialog');

            //
            $('#modal-modification_cours').modal();

            //gestion du clique sur valider les modifications
            $("#btn_save_modification_cours").on('click', function () {
                let formulaire = $('#form_update_cours');
                let href = formulaire.attr('action');

                // Déclaration de formData au niveau de la portée de la fonction
                let formData = new FormData();

                let titre = $('#edit_titre').val().trim();
                let type_cours_id = $('#edit_type_cours_id').val().trim();
                let cours_video = $('#edit_cours_video').val().trim();
                let cours_audio = $('#edit_cours_audio').val().trim();
                let cours_texte = $('#edit_cours_texte').val().trim();

                let is_valid = true;

                $('.form-group').removeClass('has-error');
                $('.error-text').hide().text('');

                if (titre === '') {
                    $('#edit_titre').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }
                if (type_cours_id === '') {
                    $('#edit_type_cours_id').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }

                let selectedOption = $('#modal-modification_cours #edit_type_cours_id option:selected');
                let type_cours_code = selectedOption.data('type_cours_code');

                if (type_cours_code === "VIDEOS" && cours_video === '') {
                    $('#edit_cours_video').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }

                if (type_cours_code === "AUDIOS" && cours_audio === '') {
                    $('#edit_cours_audio').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }

                if (type_cours_code === "TEXTES" && cours_texte === '') {
                    $('#edit_cours_texte').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }

                // Récupérer le bon input file en fonction du type choisi
                let coursFichierInput = "";
                if (type_cours_code === "VIDEOS") coursFichierInput = $('#form_update_cours #edit_cours_video');
                if (type_cours_code === "AUDIOS") coursFichierInput = $('#form_update_cours #edit_cours_audio');
                if (type_cours_code === "TEXTES") coursFichierInput = $('#form_update_cours #edit_cours_texte');

                let files = [];
                if (coursFichierInput.length > 0) {
                    files = coursFichierInput[0].files;
                }

                if (is_valid) {
                    let n = noty({
                        text: 'Voulez-vous vraiment enregistrer modifier ce cours de la session de formation ?',
                        type: 'warning',
                        dismissQueue: true,
                        layout: 'center',
                        theme: 'defaultTheme',
                        buttons: [
                            {
                                addClass: 'btn btn-primary', text: 'Valider', onClick: function ($noty) {
                                    $noty.close();

                                    // Use serializeArray() which is more reliable
                                    let form_data_array = formulaire.serializeArray();
                                    $.each(form_data_array, function (index, obj) {
                                        formData.append(obj.name, obj.value);
                                    });

                                    // Ajout du fichier correctement
                                    if (files.length > 0) {
                                        formData.append(coursFichierInput.attr('name'), files[0]);
                                    }

                                    $.ajax({
                                        type: 'post',
                                        url: href,
                                        data: formData,
                                        processData: false,
                                        contentType: false,
                                        success: function (response) {
                                            if (response.statut == 1) {
                                                resetFields('#' + formulaire.attr('id'));
                                                notifySuccess(response.message, function () {
                                                    location.reload();
                                                });
                                            }
                                            if (response.statut == 0) {
                                                let errors_list_to_display = '';

                                                for (let field in response.errors) {
                                                    let messages = response.errors[field].join('<br/>');
                                                    errors_list_to_display += `<br/><i class="fa fa-arrow-circle-right"></i> ${messages}`;
                                                    $('#' + field).addClass('is-invalid');
                                                }

                                                $('#modal-modification_cours .alert .message').html(errors_list_to_display);
                                                $('#modal-modification_cours .alert').removeClass('hidden').show();
                                            }
                                        },
                                        error: function (request, status, error) {
                                            notifyWarning("Erreur lors de l'enregistrement");
                                        }
                                    });
                                }
                            },
                            {
                                addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                                    $noty.close();
                                }
                            }
                        ]
                    });
                } else {
                    notifyWarning('Veuillez renseigner correctement le formulaire');
                }
            });

        });
    });

    $(document).on('click', '.btn_detail_cours', function () {
        let model_name = $(this).attr('data-model_name');
        let modal_title = $(this).attr('data-modal_title');
        let href = $(this).attr('data-href');

        $('#eden_std_dialog_box').load(href, function () {

            $('#modal-detail_cours').attr('data-backdrop', 'static').attr('data-keyboard', false);

            $('#modal-detail_cours').find('#btn_valider').attr({ 'data-model_name': model_name, 'data-href': href });
            $('#modal-detail_cours').find('.modal-dialog');

            //
            $('#modal-detail_cours').modal();

        });
    });

    $(document).on('click', '.btn_activer_cours', function () {
        let cours_id = $(this).data('cours_id');

        let n = noty({
            text: 'Voulez-vous vraiment activer ce cours de formation ?',
            type: 'warning',
            dismissQueue: true,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'btn btn-primary', text: 'Activer', onClick: function ($noty) {
                        $noty.close();

                        //effectuer l'activation
                        $.ajax({
                            url: '/dashboard/sessions/cours/activer',
                            type: 'post',
                            data: { cours_id: cours_id },
                            headers: { 'X-CSRFToken': getCookie('csrftoken') },
                            success: function (response) {
                                if (response.statut == 1) {
                                    notifySuccess(response.message, function () {
                                        location.reload();
                                    });
                                }
                            },
                            error: function () {
                                notifyWarning("Erreur lors de l'activation");
                            }
                        });

                    }
                },
                {
                    addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                        //annuler la suppression
                        $noty.close();
                    }
                }
            ]
        });
    });

    $(document).on('click', '.btn_supprimer_cours', function () {
        let cours_id = $(this).data('cours_id');

        let n = noty({
            text: 'Voulez-vous vraiment supprimer ce cours de formation ?',
            type: 'warning',
            dismissQueue: true,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'btn btn-primary', text: 'Supprimer', onClick: function ($noty) {
                        $noty.close();

                        //effectuer la suppression
                        $.ajax({
                            url: '/dashboard/sessions/cours/delete',
                            type: 'post',
                            data: { cours_id: cours_id },
                            headers: { 'X-CSRFToken': getCookie('csrftoken') },
                            success: function (response) {
                                if (response.statut == 1) {
                                    notifySuccess(response.message, function () {
                                        location.reload();
                                    });
                                }
                            },
                            error: function () {
                                notifyWarning('Erreur lors de la suppression');
                            }
                        });

                    }
                },
                {
                    addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                        //annuler la suppression
                        $noty.close();
                    }
                }
            ]
        });
    });
    /* TODO COURS DE LA SESSION DE FORMATION FIN */

    /* TODO CHEMINANTS DE LA SESSION DE FORMATION DEBUT */
    $(document).on('click', "#btn_save_cheminant", function () {
        let formulaire = $('#form_add_cheminant');
        let href = formulaire.attr('action');

        // Déclaration de formData au niveau de la portée de la fonction
        let formData = new FormData();

        let cheminantFichierInput = $('#form_add_cheminant #photo');

        let files = [];
        if (cheminantFichierInput.length > 0) {
            files = cheminantFichierInput[0].files;
        }

        // Validation manuelle des champs requis
        let certificat_id = $('#certificat_id').val().trim();
        let nom = $('#nom').val().trim();
        let prenoms = $('#prenoms').val().trim();
        let sexe = $('#sexe').val().trim();
        let telephone = $('#telephone').val().trim();
        let situation_matrimoniale = $('#situation_matrimoniale').val().trim();
        let departement_id = $('#departement_id').val().trim();
        let date_naissance = $('#date_naissance').val().trim();
        let tribu_id = $('#tribu_id').val().trim();
        let quartier_id = $('#quartier_id').val().trim();

        // Variable pour vérifier si tout est valide
        let is_valid = true;

        // Masquer toutes les erreurs et enlever les classes d'erreur
        $('.form-group').removeClass('has-error');

        if (certificat_id === '') {
            $('#certificat_id').closest('.form-group').addClass('has-error');
            is_valid = false;
        }
        if (nom === '') {
            $('#nom').closest('.form-group').addClass('has-error');
            is_valid = false;
        }
        if (prenoms === '') {
            $('#prenoms').closest('.form-group').addClass('has-error');
            is_valid = false;
        }
        if (sexe === '') {
            $('#sexe').closest('.form-group').addClass('has-error');
            is_valid = false;
        }
        if (telephone === '') {
            $('#telephone').closest('.form-group').addClass('has-error');
            is_valid = false;
        }
        if (situation_matrimoniale === '') {
            $('#situation_matrimoniale').closest('.form-group').addClass('has-error');
            is_valid = false;
        }
        if (departement_id === '') {
            $('#departement_id').closest('.form-group').addClass('has-error');
            is_valid = false;
        }
        if (date_naissance === '') {
            $('#date_naissance').closest('.form-group').addClass('has-error');
            is_valid = false;
        }
        if (tribu_id === '') {
            $('#tribu_id').closest('.form-group').addClass('has-error');
            is_valid = false;
        }
        if (quartier_id === '') {
            $('#quartier_id').closest('.form-group').addClass('has-error');
            is_valid = false;
        }

        if (is_valid) {
            let n = noty({
                text: 'Voulez-vous vraiment enregistrer ce cheminant ?',
                type: 'warning',
                dismissQueue: true,
                layout: 'center',
                theme: 'defaultTheme',
                buttons: [
                    {
                        addClass: 'btn btn-primary', text: 'Valider', onClick: function ($noty) {
                            $noty.close();

                            // Use serializeArray() which is more reliable
                            let form_data_array = formulaire.serializeArray();
                            $.each(form_data_array, function (index, obj) {
                                formData.append(obj.name, obj.value);
                            });

                            // Ajout du fichier correctement
                            if (files.length > 0) {
                                formData.append(cheminantFichierInput.attr('name'), files[0]);
                            }

                            $.ajax({
                                type: 'post',
                                url: href,
                                data: formData,
                                processData: false,
                                contentType: false,
                                success: function (response) {
                                    if (response.statut == 1) {
                                        resetFields('#' + formulaire.attr('id'));
                                        notifySuccess(response.message, function () {
                                            location.reload();
                                        });
                                    }
                                    if (response.statut == 0) {
                                        let errors_list_to_display = '';

                                        for (let field in response.errors) {
                                            let messages = response.errors[field].join('<br/>');
                                            errors_list_to_display += `<br/><i class="fa fa-arrow-circle-right"></i> ${messages}`;

                                            // Mettre en rouge le champ concerné
                                            $('#' + field).addClass('is-invalid');
                                        }

                                        // Afficher les erreurs dans l'alerte
                                        $('#modal-add_cheminant .alert .message').html(errors_list_to_display);
                                        $('#modal-add_cheminant .alert').removeClass('hidden').show();
                                        console.log('errors_list_to_display : ', errors_list_to_display);
                                    }
                                },
                                error: function (request, status, error) {
                                    notifyWarning("Erreur lors de l'enregistrement");
                                }
                            });
                        }
                    },
                    {
                        addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                            $noty.close();
                        }
                    }
                ]
            });
        } else {
            notifyWarning('Veuillez renseigner correctement le formulaire');
        }
    });

    $(document).on('click', '.btn_modifier_cheminant', function () {
        let model_name = $(this).attr('data-model_name');
        let modal_title = $(this).attr('data-modal_title');
        let href = $(this).attr('data-href');

        $('#eden_std_dialog_box').load(href, function () {

            manage_update_type_cours_change()

            $('#modal-modification_cheminant').attr('data-backdrop', 'static').attr('data-keyboard', false);

            $('#modal-modification_cheminant').find('#btn_valider').attr({ 'data-model_name': model_name, 'data-href': href });
            $('#modal-modification_cheminant').find('.modal-dialog');

            //
            $('#modal-modification_cheminant').modal();

            //gestion du clique sur valider les modifications
            $("#btn_save_modification_cheminant").on('click', function () {
                let formulaire = $('#form_update_cheminant');
                let href = formulaire.attr('action');

                // Déclaration de formData au niveau de la portée de la fonction
                let formData = new FormData();

                let certificat_id = $('#edit_certificat_id').val().trim();
                let nom = $('#edit_nom').val().trim();
                let prenoms = $('#edit_prenoms').val().trim();
                let sexe = $('#edit_sexe').val().trim();
                let telephone = $('#edit_telephone').val().trim();
                let situation_matrimoniale = $('#edit_situation_matrimoniale').val().trim();
                let departement_id = $('#edit_departement_id').val().trim();
                let date_naissance = $('#edit_date_naissance').val().trim();
                let tribu_id = $('#edit_tribu_id').val().trim();
                let quartier_id = $('#edit_quartier_id').val().trim();

                let is_valid = true;

                $('.form-group').removeClass('has-error');
                $('.error-text').hide().text('');

                if (nom === '') {
                    $('#edit_nom').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }
                if (prenoms === '') {
                    $('#edit_prenoms').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }
                if (sexe === '') {
                    $('#edit_sexe').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }
                if (telephone === '') {
                    $('#edit_telephone').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }
                if (situation_matrimoniale === '') {
                    $('#edit_situation_matrimoniale').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }
                if (departement_id === '') {
                    $('#edit_departement_id').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }
                if (date_naissance === '') {
                    $('#edit_date_naissance').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }
                if (tribu_id === '') {
                    $('#edit_tribu_id').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }
                if (quartier_id === '') {
                    $('#edit_quartier_id').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }

                // Récupérer le bon input file en fonction du type choisi
                let CheminantFichierInput = $('#form_update_cheminant #edit_photo');

                let files = [];
                if (CheminantFichierInput.length > 0) {
                    files = CheminantFichierInput[0].files;
                }

                if (is_valid) {
                    let n = noty({
                        text: 'Voulez-vous vraiment enregistrer modifier ce cheminant ?',
                        type: 'warning',
                        dismissQueue: true,
                        layout: 'center',
                        theme: 'defaultTheme',
                        buttons: [
                            {
                                addClass: 'btn btn-primary', text: 'Valider', onClick: function ($noty) {
                                    $noty.close();

                                    // Use serializeArray() which is more reliable
                                    let form_data_array = formulaire.serializeArray();
                                    $.each(form_data_array, function (index, obj) {
                                        formData.append(obj.name, obj.value);
                                    });

                                    // Ajout du fichier correctement
                                    if (files.length > 0) {
                                        formData.append(CheminantFichierInput.attr('name'), files[0]);
                                    }

                                    $.ajax({
                                        type: 'post',
                                        url: href,
                                        data: formData,
                                        processData: false,
                                        contentType: false,
                                        success: function (response) {
                                            if (response.statut == 1) {
                                                resetFields('#' + formulaire.attr('id'));
                                                notifySuccess(response.message, function () {
                                                    location.reload();
                                                });
                                            }
                                            if (response.statut == 0) {
                                                let errors_list_to_display = '';

                                                for (let field in response.errors) {
                                                    let messages = response.errors[field].join('<br/>');
                                                    errors_list_to_display += `<br/><i class="fa fa-arrow-circle-right"></i> ${messages}`;
                                                    $('#' + field).addClass('is-invalid');
                                                }

                                                $('#modal-modification_cheminant .alert .message').html(errors_list_to_display);
                                                $('#modal-modification_cheminant .alert').removeClass('hidden').show();
                                            }
                                        },
                                        error: function (request, status, error) {
                                            notifyWarning("Erreur lors de l'enregistrement");
                                        }
                                    });
                                }
                            },
                            {
                                addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                                    $noty.close();
                                }
                            }
                        ]
                    });
                } else {
                    notifyWarning('Veuillez renseigner correctement le formulaire');
                }
            });

        });
    });

    $(document).on('click', '.btn_supprimer_cheminant', function () {
        let cheminant_id = $(this).data('cheminant_id');

        let n = noty({
            text: 'Voulez-vous vraiment supprimer ce cheminant ?',
            type: 'warning',
            dismissQueue: true,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'btn btn-primary', text: 'Supprimer', onClick: function ($noty) {
                        $noty.close();

                        //effectuer la suppression
                        $.ajax({
                            url: '/dashboard/sessions/cheminants/delete',
                            type: 'post',
                            data: { cheminant_id: cheminant_id },
                            headers: { 'X-CSRFToken': getCookie('csrftoken') },
                            success: function (response) {
                                if (response.statut == 1) {
                                    notifySuccess(response.message, function () {
                                        location.reload();
                                    });
                                }
                            },
                            error: function () {
                                notifyWarning('Erreur lors de la suppression');
                            }
                        });

                    }
                },
                {
                    addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                        //annuler la suppression
                        $noty.close();
                    }
                }
            ]
        });
    });
    /* TODO CHEMINANTS DE LA SESSION DE FORMATION FIN */

    /* TODO QCM DU COURS DEBUT */
    let questionCounter = 0;

    function addQuestion(containerId) {
        let container = document.getElementById(containerId);
        let firstBlock = container.querySelector(".question_block");
        if (!firstBlock) return;

        let qcmClone = firstBlock.cloneNode(true);

        questionCounter++;

        // Mise à jour des noms avec l'index
        let questionInput = qcmClone.querySelector(".questions");
        questionInput.name = `questions[${questionCounter}]`;
        questionInput.id = `questions_${questionCounter}`;
        questionInput.value = "";

        // Mise à jour des inputs/réponses
        let tbody = qcmClone.querySelector("tbody");
        tbody.id = `table_body_${questionCounter}`;
        let table = qcmClone.querySelector("table");
        table.id = `table_reponses_${questionCounter}`;

        tbody.querySelectorAll("tr").forEach((tr) => {
            tr.querySelectorAll("input, select").forEach((input) => {
                if (input.classList.contains("reponses")) {
                    input.name = `reponses[${questionCounter}][]`;
                }
                if (input.classList.contains("type_reponses")) {
                    input.name = `type_reponses[${questionCounter}][]`;
                }
                if (input.classList.contains("points")) {
                    input.name = `points[${questionCounter}][]`;
                }
                input.value = "";
            });
        });

        container.appendChild(qcmClone);
    }

    function addReponse(tbody) {
        let firstTr = tbody.querySelector("tr");
        if (!firstTr) return;

        let trClone = firstTr.cloneNode(true);

        trClone.querySelectorAll("input, select").forEach((input) => {
            input.value = "";
        });

        tbody.appendChild(trClone);
    }

    function removeReponse(btn) {
        let tbody = btn.closest("tbody");
        if (tbody && tbody.childElementCount > 1) {
            btn.closest("tr").remove();
        } else {
            console.log("Impossible de supprimer la dernière réponse !");
        }
    }

    function removeQuestion(btn) {
        let container = document.getElementById("questions_reponses");
        if (container.querySelectorAll(".question_block").length > 1) {
            btn.closest(".question_block").remove();
        } else {
            console.log("Impossible de supprimer la dernière question !");
        }
    }

    $(document).on("click", ".btn_add_question", function () {
        addQuestion("questions_reponses");
    });

    $(document).on("click", ".btn_remove_question", function () {
        removeQuestion(this);
    });

    $(document).on("click", ".action_container .btn-success", function () {
        let tbody = $(this).closest("table").find("tbody")[0];
        addReponse(tbody);
    });

    $(document).on("click", ".action_container .btn-danger", function () {
        removeReponse(this);
    });

    $(document).on("change", ".type_reponses", function () {
        let tr = $(this).closest("tr");
        let pointsInput = tr.find(".points");

        if ($(this).val().toLowerCase() === "faux") {
            pointsInput.val(0).prop("readonly", true).addClass("bg-light");
        } else {
            pointsInput.prop("readonly", false).removeClass("bg-light");
            pointsInput.val("");
        }
    });

    $(document).on("input", ".points", function () {
        let val = parseInt($(this).val(), 10);
        if (val > 20) $(this).val(20);
        if (val < 0 || isNaN(val)) $(this).val("");
    });

    $(document).on('click', "#btn_save_question_reponse", function () {
        let formulaire = $('#form_add_question_reponse');
        let href = formulaire.attr('action');

        let formData = new FormData();

        let add_qcm_cours_id = $('#add_qcm_cours_id').val().trim();

        let is_valid = true;

        $('.form-group').removeClass('has-error');
        $('.error-text').hide().text('');

        if (add_qcm_cours_id === '') {
            $('#add_qcm_cours_id').closest('.form-group').addClass('has-error');
            is_valid = false;
        }

        if (is_valid) {
            let n = noty({
                text: 'Voulez-vous vraiment enregistrer les QCM du cours ?',
                type: 'warning',
                dismissQueue: true,
                layout: 'center',
                theme: 'defaultTheme',
                buttons: [
                    {
                        addClass: 'btn btn-primary', text: 'Valider', onClick: function ($noty) {
                            $noty.close();

                            let data_serialized = formulaire.serialize();
                            $.each(data_serialized.split('&'), function (index, elem) {
                                let vals = elem.split('=');
                                let key = vals[0];
                                let valeur = decodeURIComponent(vals[1].replace(/\+/g, '  '));
                                formData.append(key, valeur);
                            });

                            $.ajax({
                                type: 'post',
                                url: href,
                                data: formData,
                                processData: false,
                                contentType: false,
                                success: function (response) {
                                    if (response.statut == 1) {
                                        resetFields('#' + formulaire.attr('id'));
                                        notifySuccess(response.message, function () {
                                            location.reload();
                                        });
                                    }
                                    if (response.statut == 0) {
                                        let errors_list_to_display = '';

                                        for (let field in response.errors) {
                                            let messages = response.errors[field].join('<br/>');
                                            errors_list_to_display += `<br/><i class="fa fa-arrow-circle-right"></i> ${messages}`;

                                            // Mettre en rouge le champ concerné
                                            $('#' + field).addClass('is-invalid');
                                        }

                                        // Afficher les erreurs dans l'alerte
                                        $('#modal-add_question_reponse .alert .message').html(errors_list_to_display);
                                        $('#modal-add_question_reponse .alert').removeClass('hidden').show();
                                        console.log('errors_list_to_display : ', errors_list_to_display);
                                    }
                                },
                                error: function (request, status, error) {
                                    notifyWarning("Erreur lors de l'enregistrement");
                                }
                            });
                        }
                    },
                    {
                        addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                            $noty.close();
                        }
                    }
                ]
            });
        } else {
            notifyWarning('Veuillez renseigner correctement le formulaire avant de continuer');
        }
    });

    $(document).on('click', '.btn_detail_qcm', function () {
        let model_name = $(this).attr('data-model_name');
        let modal_title = $(this).attr('data-modal_title');
        let href = $(this).attr('data-href');

        $('#eden_std_dialog_box').load(href, function () {

            $('#modal-detail_qcm').attr('data-backdrop', 'static').attr('data-keyboard', false);

            $('#modal-detail_qcm').find('#btn_valider').attr({ 'data-model_name': model_name, 'data-href': href });
            $('#modal-detail_qcm').find('.modal-dialog');

            //
            $('#modal-detail_qcm').modal();

        });
    });

    $(document).on('click', '.btn_modifier_qcm_cours', function () {
        let model_name = $(this).attr('data-model_name');
        let modal_title = $(this).attr('data-modal_title');
        let href = $(this).attr('data-href');

        $('#eden_std_dialog_box').load(href, function () {

            $('#modal-modification_question_reponse').attr('data-backdrop', 'static').attr('data-keyboard', false);

            $('#modal-modification_question_reponse').find('#btn_valider').attr({ 'data-model_name': model_name, 'data-href': href });
            $('#modal-modification_question_reponse').find('.modal-dialog');

            //
            $('#modal-modification_question_reponse').modal();

            //gestion du clique sur valider les modifications
            $("#btn_save_modification_question_reponse").on('click', function () {
                let formulaire = $('#form_update_question_reponse');
                let href = formulaire.attr('action');

                // Déclaration de formData au niveau de la portée de la fonction
                let formData = new FormData();

                let question = $('#question').val().trim();

                let is_valid = true;

                $('.form-group').removeClass('has-error');
                $('.error-text').hide().text('');

                if (question === '') {
                    $('#question').closest('.form-group').addClass('has-error');
                    is_valid = false;
                }

                if (is_valid) {
                    let n = noty({
                        text: 'Voulez-vous vraiment modifier cette question ?',
                        type: 'warning',
                        dismissQueue: true,
                        layout: 'center',
                        theme: 'defaultTheme',
                        buttons: [
                            {
                                addClass: 'btn btn-primary', text: 'Valider', onClick: function ($noty) {
                                    $noty.close();

                                    // 👉 Correction : on envoie directement tout le formulaire
                                    let formData = new FormData(formulaire[0]);

                                    $.ajax({
                                        type: 'post',
                                        url: href,
                                        data: formData,
                                        processData: false,
                                        contentType: false,
                                        success: function (response) {
                                            if (response.statut == 1) {
                                                resetFields('#' + formulaire.attr('id'));
                                                notifySuccess(response.message, function () {
                                                    location.reload();
                                                });
                                            }
                                            if (response.statut == 0) {
                                                let errors_list_to_display = '';

                                                for (let field in response.errors) {
                                                    let messages = response.errors[field].join('<br/>');
                                                    errors_list_to_display += `<br/><i class="fa fa-arrow-circle-right"></i> ${messages}`;

                                                    // Mettre en rouge le champ concerné
                                                    $('#' + field).addClass('is-invalid');
                                                }

                                                // Afficher les erreurs dans l'alerte (CORRIGÉ: référence au bon modal)
                                                $('#modal-modification_question_reponse .alert .message').html(errors_list_to_display);
                                                $('#modal-modification_question_reponse .alert').removeClass('hidden').show();
                                                console.log('errors_list_to_display : ', errors_list_to_display);
                                            }
                                        },
                                        error: function (request, status, error) {
                                            notifyWarning("Erreur lors de l'enregistrement");
                                        }
                                    });
                                }
                            },
                            {
                                addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                                    $noty.close();
                                }
                            }
                        ]
                    });
                } else {
                    notifyWarning('Veuillez renseigner correctement le formulaire');
                }
            });

        });
    });

    $(document).on('click', '.btn_supprimer_qcm_cours', function () {
        let qcm_cours_id = $(this).data('qcm_cours_id');

        let n = noty({
            text: 'Voulez-vous vraiment supprimer cette question ?',
            type: 'warning',
            dismissQueue: true,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'btn btn-primary', text: 'Supprimer', onClick: function ($noty) {
                        $noty.close();

                        //effectuer la suppression
                        $.ajax({
                            url: '/dashboard/sessions/qcm-cours-session/delete',
                            type: 'post',
                            data: { qcm_cours_id: qcm_cours_id },
                            headers: { 'X-CSRFToken': getCookie('csrftoken') },
                            success: function (response) {
                                if (response.statut == 1) {
                                    notifySuccess(response.message, function () {
                                        location.reload();
                                    });
                                }
                            },
                            error: function () {
                                notifyWarning('Erreur lors de la suppression');
                            }
                        });

                    }
                },
                {
                    addClass: 'btn btn-danger', text: 'Annuler', onClick: function ($noty) {
                        //annuler la suppression
                        $noty.close();
                    }
                }
            ]
        });
    });
    /* TODO QCM DU COURS FIN */


    // Écouteur d'événement pour retirer la bordure rouge et le message d'erreur, dès que l'utilisateur commence à taper dans le champ.
    $(document).on('keyup change', '.form-control, input, select, textarea', function() {
        let $field = $(this);
        let fieldId = $field.attr('id');

        // Retirer la classe is-invalid du champ
        if ($field.hasClass('is-invalid')) {
            $field.removeClass('is-invalid');
        }

        // Retirer la classe has-error du form-group parent
        $field.closest('.form-group').removeClass('has-error');

        // Masquer le message d'erreur spécifique au champ
        if (fieldId) {
            $('.' + fieldId + '_error').hide().text('');
        }

        // Masquer aussi les messages d'erreur génériques
        $field.closest('.form-group').find('.error-text').hide().text('');
    });

});