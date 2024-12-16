/**
 *
 * This file only contains scripts relevant to the function of the ui. (Opening, Closing, resizing etc)
 *
 */

Number.prototype.clamp = function (min, max) {
  return Math.min(Math.max(this, min), max)
}
Number.prototype.round = function (decimals) {
  return Math.round(this * 10 ** decimals) / 10 ** decimals
}

$(document).ready(_ => {
  /*\
   * ===========================
   * Switch between Login/Signup
   * ===========================
  \*/
  $('.login.select').on('click', event => {
    $('.inner>.login')
      .removeClass('hidden')
      .animate({ opacity: 1 }, { duration: 200 })
    $('.inner>.register').css('opacity', '0%').addClass('hidden')
    $('.login.select').addClass('selected')
    $('.register.select').removeClass('selected')
  })
  $('.register.select').on('click', event => {
    $('.inner>.register')
      .removeClass('hidden')
      .animate({ opacity: 1 }, { duration: 200 })
    $('.inner>.login').css('opacity', '0%').addClass('hidden')
    $('.register.select').addClass('selected')
    $('.login.select').removeClass('selected')
  })
})
