var loadEditor = function() {
    var e = new Editor()
    var element = $('.editor').get(0)
    e.render(element)
    return e
}

var __main = function() {
    loadEditor()
}

$(document).ready(function() {
    __main()
})