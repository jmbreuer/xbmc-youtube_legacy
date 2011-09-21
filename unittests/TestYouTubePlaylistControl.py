# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys, io
from  YouTubePlaylistControl import YouTubePlaylistControl 

class TestYouTubePlaylistControl(BaseTestCase.BaseTestCase):
	
	def test_playAll_should_call_getPlayList_if_playlist_entry_in_params(self):
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = ""
		
		control.playAll({"playlist":"someid"})
		
		control.getPlayList.assert_called_with({"playlist":"someid", 'fetch_all': 'true'})
		
	def test_playAll_should_call_getDiscoSearch_if_scraper_is_disco_search_in_params(self):
		control = YouTubePlaylistControl()
		control.getDiscoSearch = Mock()
		control.getDiscoSearch.return_value = ""
		
		control.playAll({"search_disco":"some_search"})
		
		control.getDiscoSearch.assert_called_with({"search":"some_search","search_disco":"some_search", 'fetch_all': 'true'})
				
	def test_playAll_should_call_getFavorites_if_user_feed_is_favorites_in_params(self):
		control = YouTubePlaylistControl()
		control.getFavorites = Mock()
		control.getFavorites.return_value = ""
		
		control.playAll({"user_feed":"favorites"})
		
		control.getFavorites.assert_called_with({"user_feed":"favorites", 'fetch_all': 'true'})
		
	def test_playAll_should_call_getWatchLater_if_scraper_is_watch_later_in_params(self):
		control = YouTubePlaylistControl()
		control.getWatchLater = Mock()
		control.getWatchLater.return_value = ""
		
		control.playAll({"scraper":"watch_later"})
		
		control.getWatchLater.assert_called_with({"scraper":"watch_later", 'fetch_all': 'true'})
		
	def test_playAll_should_call_getLikedVideos_if_scraper_is_liked_videos_in_params(self):
		control = YouTubePlaylistControl()
		control.getLikedVideos = Mock()
		control.getLikedVideos.return_value = ""
		
		control.playAll({"scraper":"liked_videos"})
		
		control.getLikedVideos.assert_called_with({"scraper":"liked_videos", 'fetch_all': 'true'})
		
	def test_playAll_should_call_getArtist_if_scraper_is_music_artist_in_params(self):		
		control = YouTubePlaylistControl()
		control.getArtist = Mock()
		control.getArtist.return_value = ""
		
		control.playAll({"scraper":"music_artists"})
		
		control.getArtist.assert_called_with({"scraper":"music_artists", 'fetch_all': 'true'})
		
	def test_playAll_should_call_getRecommended_if_scraper_is_recommended_in_params(self):
		control = YouTubePlaylistControl()
		control.getRecommended = Mock()
		control.getRecommended.return_value = ""
		
		control.playAll({"scraper":"recommended"})
		
		control.getRecommended.assert_called_with({"scraper":"recommended", 'fetch_all': 'true'})
		
	def test_playAll_should_call_getNewSubscriptions_if_user_feed_is_subscriptions_in_params(self):
		control = YouTubePlaylistControl()
		control.getNewSubscriptions = Mock()
		control.getNewSubscriptions.return_value = ""
		
		control.playAll({"user_feed":"newsubscriptions"})
		
		control.getNewSubscriptions.assert_called_with({"user_feed":"newsubscriptions", 'fetch_all': 'true'})
		
	def test_playAll_should_not_call_xbmc_player_if_params_is_empty(self):
		sys.modules["xbmc"].Player = Mock()
		control = YouTubePlaylistControl()
		
		control.playAll({})
		
		assert(sys.modules["xbmc"].Player.call_count == 0)
		assert(sys.modules["xbmc"].Player().call_count == 0)
		
	def test_playAll_should_call_xbmc_player_stop_if_player_is_playing(self):
		sys.modules["xbmc"].Player = Mock()
		sys.modules["xbmc"].PlayList = Mock()
		sys.modules["xbmc"].PLAYLIST_VIDEO = Mock()
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle", "videoid":"some_id","thumbnail":"some_thumbnail"}]
		
		control.playAll({"playlist":"someid"})
		
		sys.modules["xbmc"].Player.assert_called_with()
		sys.modules["xbmc"].Player().isPlaying.assert_called_with()
		sys.modules["xbmc"].Player().stop.assert_called_with()
		
	def test_playAll_should_call_xbmc_PlayList_clear_if_results_is_not_empty(self):
		playlist_value = Mock()
		sys.modules["xbmc"].Player = Mock()
		sys.modules["xbmc"].PlayList = Mock()
		sys.modules["xbmc"].PlayList.return_value = playlist_value
		sys.modules["xbmc"].PLAYLIST_VIDEO = Mock()
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle", "videoid":"some_id","thumbnail":"some_thumbnail"}]
		
		control.playAll({"playlist":"someid"})
		
		playlist_value.clear.assert_called_with()
		
	def test_playAll_should_call_xbmc_player_shuffle_if_shuffle_is_in_params(self):
		playlist_value = Mock()
		sys.modules["xbmc"].Player = Mock()
		sys.modules["xbmc"].PlayList = Mock()
		sys.modules["xbmc"].PlayList.return_value = playlist_value
		sys.modules["xbmc"].PLAYLIST_VIDEO = Mock()
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle", "videoid":"some_id","thumbnail":"some_thumbnail"}]
		
		control.playAll({"playlist":"someid","shuffle":"true"})
		
		sys.modules["xbmc"].Player.assert_called_with()
		sys.modules["xbmc"].Player().isPlaying.assert_called_with()
		sys.modules["xbmc"].Player().stop.assert_called_with()
		playlist_value.shuffle.assert_called_with()
		
	def test_playAll_should_correctly_queue_all_items_in_result_list(self):
		playlist_value = Mock()
		sys.modules["xbmc"].Player = Mock()
		sys.modules["xbmc"].PlayList = Mock()
		sys.modules["xbmc"].PlayList.return_value = playlist_value
		sys.modules["xbmc"].PLAYLIST_VIDEO = Mock()
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
		
		control.playAll({"playlist":"someid","shuffle":"true"})
		
		assert(playlist_value.add.call_count == 2)
	
	def test_playAll_should_start_playback_of_playlist_if_result_list_is_not_empty(self):
		playlist_value = Mock()
		sys.modules["xbmc"].Player = Mock()
		sys.modules["xbmc"].PlayList = Mock()
		sys.modules["xbmc"].PlayList.return_value = playlist_value
		sys.modules["xbmc"].PLAYLIST_VIDEO = Mock()
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
		
		control.playAll({"playlist":"someid"})
		
		sys.modules["xbmc"].executebuiltin.assert_called_with('playlist.playoffset(video , 0)')
		
	def test_queueVideo_should_handle_a_list_of_video_ids_seperated_by_a_comma(self):
		playlist_value = Mock()
		sys.modules["xbmc"].Player = Mock()
		sys.modules["xbmc"].PlayList = Mock()
		sys.modules["xbmc"].PlayList.return_value = playlist_value
		sys.modules["xbmc"].PLAYLIST_VIDEO = Mock()
		sys.modules["__main__"].core.getBatchDetails.return_value = ({"apierror":""},303)
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
		
		control.queueVideo({"videoid":"someid1,someid2,someid3"})
		
		sys.modules["__main__"].core.getBatchDetails.assert_called_with(['someid1', 'someid2', 'someid3'], {'videoid': 'someid1,someid2,someid3'})		

	def test_queueVideo_should_call_get_batch_details_for_the_video_list(self):
		playlist_value = Mock()
		sys.modules["xbmc"].Player = Mock()
		sys.modules["xbmc"].PlayList = Mock()
		sys.modules["xbmc"].PlayList.return_value = playlist_value
		sys.modules["xbmc"].PLAYLIST_VIDEO = Mock()
		sys.modules["__main__"].core.getBatchDetails.return_value = ({"apierror":""},303)
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
		
		control.queueVideo({"videoid":"someid1,someid2,someid3"})
		
		sys.modules["__main__"].core.getBatchDetails.assert_called_with(['someid1', 'someid2', 'someid3'], {'videoid': 'someid1,someid2,someid3'})		

	def test_queueVideo_should_show_error_message_if_get_batch_details_fails(self):
		playlist_value = Mock()
		sys.modules["xbmc"].Player = Mock()
		sys.modules["xbmc"].PlayList = Mock()
		sys.modules["xbmc"].PlayList.return_value = playlist_value
		sys.modules["xbmc"].PLAYLIST_VIDEO = Mock()
		sys.modules["__main__"].language.return_value = ""
		sys.modules["__main__"].core.getBatchDetails.return_value = ([],303)
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
		
		control.queueVideo({"videoid":"someid1,someid2,someid3"})
		
		sys.modules["__main__"].utils.showErrorMessage.assert_called_with("","apierror",303)

	def test_queueVideo_should_correctly_queue_all_items_in_result_list(self):
		playlist_value = Mock()
		sys.modules["xbmc"].Player = Mock()
		sys.modules["xbmc"].PlayList = Mock()
		sys.modules["xbmc"].PlayList.return_value = playlist_value
		sys.modules["xbmc"].PLAYLIST_VIDEO = Mock()
		sys.modules["__main__"].language.return_value = ""
		sys.modules["__main__"].core.getBatchDetails.return_value = ([{"Title":"someTitle1","videoid":"some_id1", "thumbnail":"thumbnail1","video_url":"some_url1"}, {"Title":"someTitle1","videoid":"some_id1", "thumbnail":"thumbnail1","video_url":"some_url1"}, {"Title":"someTitle1","videoid":"some_id1", "thumbnail":"thumbnail1","video_url":"some_url1"}], 200)
		sys.modules["__main__"].utils.makeAscii.return_value = ""
		control = YouTubePlaylistControl()
		control.getPlayList = Mock()
		control.getPlayList.return_value = [{"Title":"someTitle1", "videoid":"some_id1","thumbnail":"some_thumbnail1"},{"Title":"someTitle2", "videoid":"some_id2","thumbnail":"some_thumbnail2"}]
		
		control.queueVideo({"videoid":"someid1,someid2,someid3"})
		
		assert(playlist_value.add.call_count == 3)

	def test_getPlayList_should_call_feeds_list_all(self):
		control = YouTubePlaylistControl()
		
		control.getPlayList({"playlist":"some_playlist"})
		
		sys.modules["__main__"].feeds.listAll.assert_called_with({'user_feed': 'playlist', 'playlist': 'some_playlist'})

	def test_getPlayList_should_exit_cleanly_if_playlist_id_is_missing_from_params(self):
		control = YouTubePlaylistControl()
		
		control.getPlayList({})
		
		assert(sys.modules["__main__"].feeds.listAll.call_count == 0)

	def ttest_getWatchLater_should_call_scraper_getWatchLater(self):
		assert(False)

	def ttest_getDiscoSearch_should_call_scraper_getDiscoSearch(self):
		assert(False)

	def ttest_getDiscoSearch_should_call_call_getBatchDetailsDisco_if_scraper_succeded(self):
		assert(False)
		
	def ttest_getFavorites_should_exit_cleanly_if_contact_is_missing(self):
		assert(False)

	def ttest_getFavorites_should_call_core_list_all_with_correct_params(self):
		assert(False)

	def ttest_getNewSubscriptions_should_exit_cleanly_if_contact_is_missing(self):
		assert(False)

	def ttest_getNewSubscriptions_should_call_core_list_all_with_correct_params(self):
		assert(False)
		
	def ttest_getRecommended_should_exit_cleanly_if_login_or_scraper_is_not_in_params(self):
		assert(False)

	def ttest_getRecommended_should_call_scraper_getRecommended(self):
		assert(False)

	def ttest_getRecommended_should_call_core_getBatchDetails_if_scraper_succeded(self):
		assert(False)

	def ttest_getArtist_should_exit_cleanly_if_artist_is_not_in_params(self):
		assert(False)

	def ttest_getArtist_should_call_scraper_scrapeArtist(self):
		assert(False)

	def ttest_getArtist_should_call_core_getBatchDetails_if_scraper_succeded(self):
		assert(False)
		
	def ttest_getLikedVideos_should_exit_cleanly_if_scraper_or_login_is_not_in_params(self):
		assert(False)
	
	def ttest_getLikedVideos_should_call_scraper_scrapeLikedVideos(self):
		assert(False)
		
	def ttest_getLikedVideos_should_call_core_getBatchDetails_if_scraper_succeded(self):
		assert(False)
		
	def ttest_addToPlaylist_should_call_list_all_if_playlist_is_not_in_params(self):
		assert(False)

	def ttest_addToPlaylist_should_ask_user_for_playlist_if_playlist_is_not_in_params(self):
		assert(False)

	def ttest_addToPlaylist_should_call_createPlaylist_if_user_selects_create_option(self):
		assert(False)

	def ttest_addToPlaylist_should_call_core_add_to_playlist_if_playlist_is_in_params(self):
		assert(False)

	def ttest_addToPlaylist_should_call_core_add_to_plaulist_if_user_has_selected_playlist(self):
		assert(False)

	def ttest_createPlayList_should_ask_user_for_input(self):
		assert(False)

	def ttest_createPlayList_should_call_addPlaylist_if_user_provided_playlist_name(self):
		assert(False)

	def ttest_removeFromPlaylist_should_exit_cleanly_if_playlist_or_editid_is_missing(self):
		assert(False)

	def ttest_removeFromPlaylist_should_call_core_remove_from_playlist(self):
		assert(False)

	def ttest_removeFromPlaylist_should_show_error_message_if_remove_call_failed(self):
		assert(False)
	
	def ttest_removeFromPlaylist_should_call_xbmc_execute_builtin_on_success(self):
		assert(False)
	
	def ttest_deletePlaylist_should_exit_cleanly_if_playlist_is_missing(self):
		assert(False)
	
	def ttest_deletePlaylist_should_call_core_delete_playlist(self):
		assert(False)
	
	def ttest_deletePlaylist_should_show_error_message_if_delete_call_failed(self):
		assert(False)
	
	def ttest_deletePlaylist_should_call_xbmc_execute_builtin_on_success(self):
		assert(False)	

if __name__ == '__main__':
	nose.run()
