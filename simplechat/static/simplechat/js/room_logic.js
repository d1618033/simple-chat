(function () {
    var last_message_pk = 0;
    var user;

    var User = function (name, url, pk, password) {
        this.name = name;
        this.url = url;
        this.pk = pk;
        this.password = password;
    };


    function delete_user() {
        $.ajax({
            url: user.url,
            method: "delete",
            data: {password: user.password}
        }).done(function () {
            go_to_home_page();
        });
    }

    function go_to_home_page() {
        location.href = urls.index;
    }

    function on_room_deletion() {
        go_to_home_page();
    }

    function update_users() {
        $.get(
            urls.room_detail,
            {},
            function (data) {
                update_users_list(data.participant_set);
            }
        ).fail(function () {
                on_room_deletion();
            })
    }

    function get_counter(x) {
        var counter = {};
        x.forEach(function (X) {
            if (counter[X] === undefined) {
                counter[X] = 1;
            } else {
                counter[X] += 1;
            }
        });
        return counter;
    }

    function get_all_keys(obj1, obj2) {
        return _.chain(_.keys(obj1))
            .union(_.keys(obj2))
            .value();
    }

    function get_diff_counters(old_counter, new_counter) {
        var to_add = {};
        var to_delete = {};
        _.each(get_all_keys(old_counter, new_counter), function (key) {
            var old_value = old_counter[key] | 0;
            var new_value = new_counter[key] | 0;
            var diff = new_value - old_value;
            if (diff > 0) {
                to_add[key] = diff;
            } else {
                to_delete[key] = -diff;
            }
        });
        return {"add": to_add, "delete": to_delete};
    }

    function add_user_to_list(name) {
        $("#people_list").append($("<li>").text(name).attr("data-name", name));
    }

    function remove_user_from_list(name, number) {
        $("#people_list").find("li").filter(function (i, e) {
            return e.getAttribute("data-name") === name;
        }).slice(0, number).remove();
    }

    function get_old_users() {
        return $("#people_list").find("li").map(function (i, e) {
            return e.textContent;
        }).toArray();
    }

    function update_users_list_add(to_add) {
        _.each(to_add, function (count, name) {
            for (var i = 0; i < count; i++) {
                add_user_to_list(name);
            }
        });
    }

    function update_users_list_delete(to_delete) {
        _.each(to_delete, function (count, name) {
            remove_user_from_list(name, count);
        });
    }

    function update_users_list(new_users) {
        var diff = get_diff_counters(get_counter(get_old_users()), get_counter(new_users));
        update_users_list_add(diff.add);
        update_users_list_delete(diff.delete);
    }

    function fix_message(message, name) {
        if (name === undefined) {
            name = user.name;
        }
        return "[" + name + "]: " + message;
    }

    function add_message_to_list(message, name) {
        message = fix_message(message, name);
        $("#message_list").append($("<li>").text(message));
        var e = $("#message_list_div");
        e.scrollTop(e.prop("scrollHeight"));
    }

    function get_message_text() {
        return $("#message")[0].value
    }

    function clear_message_text() {
        $("#message")[0].value = "";
    }

    function on_click_send_message() {
        var message = get_message_text();
        post_message_to_server(message);
        clear_message_text();
    }

    function on_keypress_message(e) {
        if (e.which == 13) {
            on_click_send_message();
            return false;
        }
    }

    function post_message_to_server(message) {
        $.post(urls.message_list,
            {
                "room": context.room_id,
                "participant": user.pk,
                "password": user.password,
                "message": message
            }
        ).done(function (data) {
                add_message_to_list(message);
            })
    }

    function update_messages() {
        $.get(urls.message_recent,
            {
                'room_pk': context.room_id,
                'from_pk': last_message_pk,
                'not_from_participant_pk': user.pk
            },
            update_message_list
        )
    }

    function update_message_list(messages) {
        if (messages.length >= 1) {
            _.each(messages, function (message) {
                console.log(message);
                add_message_to_list(message.message, message.name);

            });
            last_message_pk = messages[messages.length - 1].pk;
        }
    }

    function pollForUsers() {
        update_users();
        setTimeout(pollForUsers, 3000);
    }

    function pollForMessages() {
        update_messages();
        setTimeout(pollForMessages, 1000);
    }

    $(document).ready(function () {
        user = new User(context.name, urls.participant, context.user_pk, context.password);
        $("#logout").click(delete_user);
        $("#message-send-btn").click(on_click_send_message);
        $("#message-label").text(fix_message(""));
        $("#greetings").text("Welcome to room " + context.room_id + ", " + user.name);
        var message_elem = $('#message');
        message_elem.keypress(on_keypress_message);
        add_user_to_list(user.name);
        message_elem.focus();
        pollForUsers();
        pollForMessages();
    });
})();