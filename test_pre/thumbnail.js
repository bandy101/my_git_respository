function zoom(mask_pop, bigimg, smallimg) {
    this.bigimg = bigimg;
    this.smallimg = smallimg;
    this.mask_pop = mask_pop
}
zoom.prototype = {
    init: function() {
        this.smallimgClick();
        this.maskClick();
    },
    smallimgClick: function() {
        var that = this;
        $("." + that.smallimg).click(function() {
            $("." + that.bigimg).css({
                height: $("." + that.smallimg).height() * 4.5,
                width: $("." + that.smallimg).width() * 4.5
            });
            $("." + that.mask_pop).fadeIn();
            $("." + that.bigimg).attr("src", $(this).attr("src")).fadeIn()
        })
    },
    maskClick: function() {
        var that = this;
        $("." + that.mask_pop).click(function() {
            $("." + that.bigimg).fadeOut();
            $("." + that.mask_pop).fadeOut()
        })
    }

};