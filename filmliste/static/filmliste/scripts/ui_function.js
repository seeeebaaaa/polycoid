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
    console.log('now it changes sth')
  })


  /*\
   * ============
   * Add new List
   * ============
  \*/
  $('.popup.new-list button.create').on("click", async event => {
    
    const title = $("#create-list-name").val()
    const colors = $(".popup.new-list .title-card").data("colors")
    console.log(title);
    
    const data = await api(FILMLISTE.addlist,{"title":title,"colors":colors},CSRF_TOKEN)
    console.log(data);
    
  })
})
