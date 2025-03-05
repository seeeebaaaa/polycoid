/**
 *
 * This document contains all scripts relted to functions of ui elements that dont rely only on style.
 *
 */

$(document).ready(_ => {
  /**
   * ===========
   * Search bars
   * ===========
   */
  $('.search-container .search-box input').on('input', event => {
    const element_container = $(event.currentTarget)
      .closest('.box')
      .find('.container .card-container')
    const search = $(event.currentTarget).val().toLocaleLowerCase()
    element_container.children().each((idx, el) => {
      const title = $(el).find('div>.text-mirror').text().toLocaleLowerCase()
      if (title.includes(search))
        $(el).show()
      else
        $(el).hide()
    })
  })

  /*\
   * ============
   * Add new List
   * ============
  \*/
  $('.popup-new-list button.create').on('click', async event => {
    const title = $('#create-list-name').val()
    const colors = $('.popup-new-list .title-card').data('colors')

    const data = await api(
      FILMLISTE.addlist,
      { title: title, colors: colors },
      CSRF_TOKEN
    )
  })

  /*\
   * ==============
   * Discover Lists
   * ==============
  \*/
  // on input send discovery request; but only every n seconds to avoid getting ratelimited
  let debounceTimeout;

  $(".popup.browse-lists .content .query .filter .search-box .input input").on("input", event => {
    const query = $(event.currentTarget).val();

    if (!userIs_authenticated) {
      $(".popup.browse-lists .content .query .error").removeClass("hidden")
      return
    }
    $(".popup.browse-lists .content .query .error").addClass("hidden")

    // Clear the previous timeout
    clearTimeout(debounceTimeout);

    // setup loading symbol
    $(".popup.browse-lists .content .cards .loading").removeClass("hidden").find("svg").addClass("spinning")

    // Set a new timeout to send the request after 2 seconds
    debounceTimeout = setTimeout(async () => {
      try {
        const data = await api(
          FILMLISTE.discoverLists,
          { query: query },
          CSRF_TOKEN,
          "GET"
        );
        response = await data.json()
        const baseCard = $(".baseCard")
        const container = $(".popup.browse-lists .content .cards")
        // remove all other cards
        container.children("a:not(.baseCard)").remove()
        // remove info texts
        container.find(".info").addClass("hidden")
        // if no results were found display none text
        if (response.results.length == 0) 
          container.find(".info.none").removeClass("hidden")
        // clone title cards and add info
        for (const result of response.results) {
          let newCard = baseCard.clone(true).removeClass("baseCard hidden")
          newCard.find(".text").text(result.title)
          newCard.find(".text-mirror").text(result.title)
          newCard.attr("href", FILMLISTE.listDetails.replace("0", result.id.toString()))
          newCard.find(".title-card").data("colors", result.colors) // note: .data manages internal data and does not set the data- dom attribute
          // append new card to card container
          newCard.appendTo(container)

          // trigger relevant functions after appending to ensure proper sizing
          newCard.find(".title-card").trigger('font-change', 1000)
          newCard.find(".title-card").trigger('set-background', null)
        }
        
        // remove laoding
        $(".popup.browse-lists .content .cards .loading").addClass("hidden").find("svg").removeClass("spinning")

        // set more notification
        if (response.has_more) {
          $(".popup.browse-lists .content .query .cards .info.more").removeClass("hidden").appendTo(container).find("span").text(response.has_more)
        }
        else
          $(".popup.browse-lists .content .query .cards .info.more").addClass("hidden")

      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }, 1000);
  });



})
