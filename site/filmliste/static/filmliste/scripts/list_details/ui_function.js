/*\
 * ============
 * List Details
 * ============
\*/

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

  /**
   * ================
   * Media Search bar
   * ================
   */

  // handle user input
  let media_search_bar_timeout;
  $('.nav .mid .search-for-media input').on('input', async event => {
    show_media_search()
    const container = $(event.currentTarget).closest(".search-for-media").find(".query-result-container")[0]
    
    // Clear the previous timeout
    clearTimeout(media_search_bar_timeout);
    media_search_bar_timeout = setTimeout(async () => {
      // make api query
      const data = await api(
        FILMLISTE.search,
        { query: $(event.currentTarget).val() },
        CSRF_TOKEN,
        method = "GET"
      )
      const result = await data.json()
      console.log(result);
    
      base_item = $(container).find(".query-item.base.hidden")
      // create media titles
      const title_container = $(container).find(".query-set.title")
      // remove old childs
      $(title_container).children().not('.base.hidden').remove()
      let max_titles = 10
      for (title of result.titles) {
        if (max_titles == 0) continue
        new_item = base_item.clone(true).removeClass("base hidden")
        new_item.find("img").attr("src", TMDB.baseURL + "w92/" + title.poster_path)
        new_item.find(".title span").text(title.media_type == "tv" ? title.name : title.title)

        new_item.appendTo(title_container)
        max_titles--
      }
    
      // create collections
      const collection_container = $(container).find(".query-set.collection")
      // remove old childs
      $(collection_container).children().not('.base.hidden').remove()
      let max_collections = 5
      for (collection of result.collections) {
        if (max_collections == 0) continue
        new_item = base_item.clone(true).removeClass("base hidden")
        new_item.find("img").attr("src", TMDB.baseURL + "w92/" + collection.poster_path)
        new_item.find(".title span").text(collection.name)

        new_item.appendTo(collection_container)
        max_collections--
      }
    },500)
  })

  // hide if clicked away
  $(document).on("click", (e) => { 
    if (!e.target.closest(".search-for-media")) { hide_media_search(); console.log(e.target.closest(".query-result-container"));
    }
  })
  // show if clicked into and already input in field
  $('.nav .mid .search-for-media input').on('focusin', async e => { 
    if ($(e.target).val()) { show_media_search(); console.log("bb");
    }
  })
})

function show_media_search() {
  const container = $(".query-result-container")
  container.find("span").removeClass("hidden")
  container.find(".query-set").removeClass("hidden")
}
function hide_media_search() {
  const container = $(".query-result-container")
  container.find("span").addClass("hidden")
  container.find(".query-set").addClass("hidden")
}

hide_media_search()