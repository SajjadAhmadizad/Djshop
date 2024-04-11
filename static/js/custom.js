function sendArticleComment(articleId) {
    var comment = $('#commentText');
    var parentId = $('#parent_id').val();
    comment = comment.val();
    // var comment = document.getElementById('commentText').value;

    console.log(comment);
    console.log(parentId);

    $.get('/articles/add-article-comment', {
        articleComment: comment,
        articleId: articleId,
        parentId: parentId
    }).then(res => {
        console.log(parentId);
        // location.reload();
        // console.log(res);
        // alert(res);
        $("#comments_area").html(res);
        $('#commentText').val('');
        $('#parent_id').val('');
        document.getElementById("comments_area").scrollIntoView({behavior: "smooth"});

        if (parentId !== null && parentId !== "") {
            document.getElementById('single_comment_box_' + parentId).scrollIntoView({behavior: 'smooth'})
        }
    });
}

function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById("comment_form").scrollIntoView({behavior: "smooth"});
}


function check_inputs() {
    var form_data = $(document.forms["contact-form"]).serialize();
    // console.log(form_data);

    $.post('', form_data, function (response) {
        // console.log(response);
        $('#control-form').html(response);
        if (response.status === 'success') {
            Swal.fire({
                title: 'اعلان',
                text: response.text,
                icon: response.icon,
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                background: '#fff',
                cancelButtonColor: '#d33',
                confirmButtonText: 'باشه ممنون!'
            })
        }
    }, "");
}

function deleteComment(id) {
    Swal.fire({
        title: 'اعلان',
        text: 'کامنت مورد نظر حذف شود؟',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        background: '#fff',
        cancelButtonColor: '#d33',
        cancelButtonText: 'خیر',
        confirmButtonText: 'بله'
    }).then((result) => {
        if (result.isConfirmed) {
            $.get('/articles/delete-article-comment', {
                comment_id: id,
                article_id: document.getElementById("article-id").value
            }).then(res => {
                // console.log(res);
                if (res.status === 'success') {
                    $("#comments_area").html(res.body);
                }
                Swal.fire({
                    title: 'اعلان',
                    text: res.text,
                    icon: res.icon,
                    showCancelButton: false,
                    confirmButtonColor: '#3085d6',
                    background: '#fff',
                    cancelButtonColor: '#d33',
                    confirmButtonText: res.confirm_button_text
                })

            })
        }
    })
}


function filterProducts() {
    // debugger;
    const filterPrice = $('#sl2').val();
    const start_price = filterPrice.split(',')[0];
    const end_price = filterPrice.split(',')[1];
    $("#start_price").val(start_price);
    $("#end_price").val(end_price);
    // =====================
    // important :
    $("#page").val(1);
    // =====================
    $("#filter_form").submit();
}


function fillPage(page) {
    $("#page").val(page);
    $("#filter_form").submit();
}


function showLargeImage(imageSrc) {
    // console.log(imageSrc);
    $("#main_image").attr('src', imageSrc);
    $("#show_large_image_modal").attr('href', imageSrc);
}


function submitProductComment() {
    var form_data = $(document.forms["product_comment_form"]).serialize();
    console.log(form_data);
    $.post("add-product-comment/", form_data, function (response) {
        // console.log(response);
        $('#product_comment_area').html(response);
        $('#comment_text').val('');
        document.getElementById("comments_top").scrollIntoView({behavior: "smooth"});
    }, "");
}


function addProductToOrder(productId) {
    var productCount = $("#product-count").val();
    if (productCount === undefined) {
        productCount = 1;
    }
    $.get('/order/add-to-order?product_id=' + productId + "&count=" + productCount).then(res => {
        Swal.fire({
            title: 'اعلان',
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: '#3085d6',
            background: '#fff',
            cancelButtonColor: '#d33',
            confirmButtonText: res.confirm_button_text
        }).then((result) => {
            if (result.isConfirmed && res.status === 'not_auth') {
                window.location.href = '/login?next='+res.url;
            }
        })
    });
}


function removeOrderDetail(detailId) {
    Swal.fire({
        title: 'اعلان',
        text: 'محصول مورد نظر از سبد خرید حذف شود؟',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        background: '#fff',
        cancelButtonColor: '#d33',
        confirmButtonText: 'بله'
    }).then((result) => {
        if (result.isConfirmed) {
            $.get('/user/remove-order-detail?detail_id=' + detailId).then(res => {
                // console.log(res);
                if (res.status === 'success') {
                    $("#order-detail-content").html(res.body);
                }
                Swal.fire({
                    title: 'اعلان',
                    text: res.text,
                    icon: res.icon,
                    showCancelButton: false,
                    confirmButtonColor: '#3085d6',
                    background: '#fff',
                    cancelButtonColor: '#d33',
                    confirmButtonText: res.confirm_button_text
                })

            })
        }
    })

}


function changOrderDetailCount(detail_id, state) {
    $.get('/user/change-order-detail-count', {
        detail_id:detail_id,
        state:state,

    }).then(res => {
        if(res.status === 'success'){
            $("#order-detail-content").html(res.body);
        }
    });
}


// const tooltipInner = document.querySelector(".tooltip-inner");
//
// const observer = new MutationObserver((mutationsList, observer) => {
//   for(let mutation of mutationsList) {
//     if (mutation.type === 'childList' && mutation.target === tooltipInner) {
//       console.log(tooltipInner.innerHTML);
//     }
//   }
// });
//
// observer.observe(tooltipInner, { childList: true });