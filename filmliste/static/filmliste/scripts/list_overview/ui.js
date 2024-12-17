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
  /**
   * ===========
   * Search bars
   * ===========
   */
  // Hide/Show input box on button press
  $('.search-container .symbol button').on('click', event => {
    // get box
    const searchBox = $(event.currentTarget)
      .closest('.search-container')
      .find('.search-box')
    const input = searchBox.find('input')
    // change width and set active
    if (searchBox.width() === 0) {
      searchBox
        .animate({ width: '7em' }, 300)
        .find('button, input')
        .attr('tabindex', 0)
      input.focus()
    } else {
      searchBox
        .animate({ width: '0em' }, 300)
        .find('button, input')
        .attr('tabindex', -1)
    }
  })
  //   Clear the input when X is pressed
  $('.search-container .search-box button').on('click', event => {
    const box = $(event.currentTarget).closest('.search-box')
    box.find('input').val('').focus().trigger('input') // trigger event to call search with empty value aka. reset
    box.find('button, input').attr('tabindex', -1)
  })
  $('.search-container .search-box input').on('focusout', event => {
    if ($(event.currentTarget).val() == '') {
      const searchBox = $(event.currentTarget)
        .closest('.search-container')
        .find('.search-box')
        .animate({ width: '0em' }, 300)
        .find('button, input')
        .attr('tabindex', -1)
    }
  })

  /*\
   * ===========
   * Title Cards
   * ===========
  \*/
  $('.title-card').on('font-change', (event, duration = 100) => {
    const title_card = $(event.currentTarget)
    const text = title_card.find('.text')
    const min_font = 0.5
    const max_font = 3
    const text_mirror = title_card.find('.text-mirror')
    const ratio =
      title_card.prop('clientHeight') / text_mirror.prop('scrollHeight')

    if (ratio > 1) {
      font_size = max_font
      break_type = 'normal'
    } else {
      font_size = Math.max((max_font - min_font) * ratio + min_font, min_font)
      break_type = 'break-all'
    }
    text.animate(
      {
        'font-size': '' + Math.round(font_size * 1000) / 1000 + 'em',
        'word-break': break_type
      },
      { duration: duration, queue: false, easing: 'easeOutCubic' }
    )
  })
  // trigger font change once after load
  $('.title-card').trigger('font-change', 1000)
  // add function that sets gradient form colors
  $('.title-card').on('set-background', (event, args) => {
    if ($(event.currentTarget).data("colors"))
      colors = $(event.currentTarget).data("colors")
    else if (args)
      colors = args.colors
    else
      return
    
    const title_card = $(event.currentTarget)
    // use first color to set background color
    title_card.css(
      'background-color',
      `hsla(${colors[0].h}, ${colors[0].s * 100}%, ${colors[0].v * 100}%, 1)`
    )
    colors = colors.slice(1)
    let gradient = ''
    for (color of colors) {
      gradient += `radial-gradient(at ${(color.x * 100).round(2)}% ${(
        color.y * 100
      ).round(2)}%, hsla(${color.h}, ${color.s * 100}%, ${
        color.v * 100
      }%, 1) 0px, transparent 50%),`
    }

    title_card.css('background-image', gradient.slice(0, -1))
  })
  // set fonts from memory on load
  $('.title-card').trigger("set-background", null)


  /*\
   * ===============
   * Create new list
   * ===============
  \*/
  // open popup
  $('.add-new-list').on('click', event => {
    $('.popup.new-list').removeClass('hidden')
    $('body>.bg-shadow').removeClass('hidden')
    $('.popup.new-list .refresh-color').trigger('click')
  })

  // mirror input + font change
  $('#create-list-name').on('input', event => {
    // set the popup title card inner text to input
    $(event.currentTarget)
      .closest('.new-list')
      .find('.title-card .text, .title-card .text-mirror')
      .text($(event.currentTarget).val())
      .trigger('font-change')
  })

  // refresh titlecard color
  $('.popup.new-list .refresh-color').on('click', event => {
    // generate random colors
    const colors = generateHSVGoldenColors(7)
    // set colorsp
    $(event.currentTarget)
    .closest('.popup')
    .find('.title-card')
    .data('colors', colors)
    .trigger('set-background', { colors: colors })
    $({deg:0}).animate(
        {
          deg: 360,
        },
      {
        duration: 750, queue: true, easing: 'easeOutCubic', step: now => {
          $(event.currentTarget).find("svg").css("transform","rotate("+now+"deg)")
        }}
      )
  })

  /*\
   * ===========
   * Popup close
   * ===========
  \*/
  $('.popup-close').on('click', event => {
    $(event.currentTarget).closest('.popup').addClass('hidden')
    $('body>.bg-shadow').addClass('hidden')
  })

  $('body>.bg-shadow').on('click', event => {
    $('.popup').addClass('hidden')
    $(event.currentTarget).addClass('hidden')
  })

  /*\
   * ===========
   * Profile Box
   * ===========
  \*/
  $('.nav>.profile>.symbol>button').on("click", event => {
    $(".profile-box").toggleClass("hidden")
    $(".bg-shadow#profile_box").toggleClass("hidden")
  })
  $('.bg-shadow#profile_box').on('click', event => {
    $('.profile-box').toggleClass('hidden')
    $(event.currentTarget).addClass('hidden')
  })
})
