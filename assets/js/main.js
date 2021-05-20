//
$(".cat-link").on("click", function (e) {
    let catid = $(this).data("id")
    let catname = $(this).find(".cat-name").html();

    let header =$("#id_content > h1").first()
    if (header.length > 0) {
        header.html(catname)
    } else {
        let h1 = $("<h1>").addClass("text-muted mt-3").html(catname)
        $("#id_content").prepend(h1)
    }
    function set_result(result) {
        $("#id_content > h1").nextAll().remove()
        $("#id_content").append(result)
    }

    set_result("<img src='/static/img/loading.gif'>")
    $.ajax({
        method: "GET",
        url: "/uz/cat-ajax/" + catid + "/",
        success: function (result) {
            set_result(result)
        },
        error: function (e) {
            set_result("<div>" + e.statusText + " [ " + e.status + "]</div>")
        }
    })

    return false;
})