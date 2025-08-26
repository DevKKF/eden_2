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