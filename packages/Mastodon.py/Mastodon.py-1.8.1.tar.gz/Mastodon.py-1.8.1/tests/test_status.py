import pytest
from mastodon.Mastodon import MastodonAPIError, MastodonNotFoundError
import datetime
try:
    import zoneinfo
    timezone = zoneinfo.ZoneInfo
except:
    import pytz
    timezone = pytz.timezone

import vcr
import time
import pickle
import os

@pytest.mark.vcr()
def test_status(status, api):
    status2 = api.status(status['id'])
    assert status2

@pytest.mark.vcr()
def test_status_reply(status, api2):
    status2 = api2.status_reply(status, "same!")
    try:
        assert status2
        assert status2.mentions[0].id == status.account.id
    finally:
        api2.status_delete(status2['id'])
        
@pytest.mark.vcr()
def test_status_empty(api):
    with pytest.raises(MastodonAPIError):
        api.status_post('')

@pytest.mark.vcr()
def test_status_missing(api):
    with pytest.raises(MastodonNotFoundError):
        api.status(0)

# Messy and will only work if there is an internet connection that is decent, obviously.
# Also, deprecated, but still a good test (Mastodon.py tries to fake the old behaviour
# internally)
@pytest.mark.vcr()
def test_status_card(api):
    import time
    status = api.status_post("http://example.org/")
    time.sleep(5) # Card generation may take time
    card = api.status_card(status['id'])
    
    try:
        assert card
        assert card.url == "http://example.org/"
    finally:
        api.status_delete(status['id'])

# Old-version card api
def test_status_card_pre_2_9_2(api):
    with vcr.use_cassette('test_status_card.yaml', cassette_library_dir='tests/cassettes_pre_2_9_2', record_mode='none'):    
        import time
        status = api.status_post("http://example.org/")
        time.sleep(5) # Card generation may take time
        api.verify_minimum_version("2.9.2", cached=False)
        card = api.status_card(status['id'])
        try:
            assert card
            assert card.url == "http://example.org/"
        finally:
            api.status_delete(status['id'])


@pytest.mark.vcr()
def test_status_context(status, api):
    context = api.status_context(status['id'])
    assert context

@pytest.mark.vcr()
def test_status_reblogged_by(status, api):
    api.status_reblog(status['id'])
    reblogs = api.status_reblogged_by(status['id'])
    assert reblogs

@pytest.mark.vcr()
def test_status_reblog_visibility(status, api):
    reblog_result = api.status_reblog(status['id'], visibility = 'unlisted')
    assert reblog_result.visibility == 'unlisted'

@pytest.mark.vcr()
def test_status_favourited_by(status, api):
    api.status_favourite(status['id'])
    favourites = api.status_favourited_by(status['id'])
    assert favourites

@pytest.mark.vcr()
def test_toot(api):
    status = api.toot('Toot!')
    try:
        assert status
    finally:
        api.status_delete(status['id'])

@pytest.mark.vcr()
@pytest.mark.parametrize('visibility', (None, 'direct', 'private', 'unlisted', 'public',
        pytest.param('foobar', marks=pytest.mark.xfail(strict=True))))
@pytest.mark.parametrize('spoiler_text', (None, 'Content warning'))
def test_status_post(api, visibility, spoiler_text):
    status = api.status_post(
            'Toot!',
            visibility=visibility,
            spoiler_text=spoiler_text)
    try:
        assert status
        if visibility:
            assert status['visibility'] == visibility
        if spoiler_text:
            assert status['spoiler_text'] == spoiler_text
    finally:
        api.status_delete(status['id'])

@pytest.mark.vcr()
def test_status_reblog_unreblog(status, api):
    reblog = api.status_reblog(status['id'])
    assert reblog

    status = reblog['reblog']
    assert status['reblogged']

    status = api.status_unreblog(status['id'])
    assert not status['reblogged']


@pytest.mark.vcr()
def test_status_fav_unfav(status, api):
    status = api.status_favourite(status['id'])
    assert status['favourited']

    status = api.status_unfavourite(status['id'])
    assert not status['favourited']

@pytest.mark.vcr()
def test_favourites(api):
    favs = api.favourites()
    assert isinstance(favs, list)


@pytest.mark.vcr()
def test_status_mute_unmute(status, api):
    status = api.status_mute(status['id'])
    assert status['muted']

    status = api.status_unmute(status['id'])
    assert not status['muted']
    
@pytest.mark.vcr()
def test_status_pin_unpin(status, api):
    status = api.status_pin(status['id'])
    assert status['pinned']

    status = api.status_unpin(status['id'])
    assert not status['pinned']

@pytest.mark.vcr(match_on=['path'])
def test_scheduled_status(api):
    base_time = datetime.datetime(4000, 1, 1, 12, 13, 14, 0, timezone("Etc/GMT+2"))
    the_future = base_time + datetime.timedelta(minutes=20)
    scheduled_toot = api.status_post("please ensure adequate headroom", scheduled_at=the_future)
    assert scheduled_toot

    the_immediate_future = base_time + datetime.timedelta(minutes=10)
    scheduled_toot_2 = api.scheduled_status_update(scheduled_toot, the_immediate_future)
    assert scheduled_toot_2
    assert scheduled_toot_2.id == scheduled_toot.id
    assert scheduled_toot_2.scheduled_at < scheduled_toot.scheduled_at

    scheduled_toot_list = api.scheduled_statuses()
    assert any(x.id == scheduled_toot_2.id for x in scheduled_toot_list)

    scheduled_toot_3 = api.scheduled_status(scheduled_toot.id)
    assert scheduled_toot_2.id == scheduled_toot_3.id

    api.scheduled_status_delete(scheduled_toot_2)
    scheduled_toot_list_2 = api.scheduled_statuses()
    assert not any(x.id == scheduled_toot_2.id for x in scheduled_toot_list_2)

    if os.path.exists("tests/cassettes/test_scheduled_status_datetimeobjects.pkl"):
        the_very_immediate_future = datetime.datetime.fromtimestamp(pickle.load(open("tests/cassettes/test_scheduled_status_datetimeobjects.pkl", 'rb')))
    else:
        the_very_immediate_future = datetime.datetime.now() + datetime.timedelta(seconds=5)
        pickle.dump(the_very_immediate_future.timestamp(), open("tests/cassettes/test_scheduled_status_datetimeobjects.pkl", 'wb'))
    scheduled_toot_4 = api.status_post("please ensure adequate headroom", scheduled_at=the_very_immediate_future)
    time.sleep(15)
    statuses = api.timeline_home()
    scheduled_toot_list_3 = api.scheduled_statuses()
    assert any(x.id == scheduled_toot_4.id for x in statuses)
    assert not any(x.id == scheduled_toot_4.id for x in scheduled_toot_list_3)

# The following two tests need to be manually (!) ran 10 minutes apart when recording.
# Sorry, I can't think of a better way to test scheduled statuses actually work as intended.
@pytest.mark.vcr(match_on=['path'])
def test_scheduled_status_long_part1(api):
    with vcr.use_cassette('test_scheduled_status_long_part1.yaml', cassette_library_dir='tests/cassettes_special', record_mode='once'):  
        if os.path.exists("tests/cassettes_special/test_scheduled_status_long_datetimeobjects.pkl"):
            the_medium_term_future = datetime.datetime.fromtimestamp(pickle.load(open("tests/cassettes_special/test_scheduled_status_long_datetimeobjects.pkl", 'rb')))
        else:
            the_medium_term_future = datetime.datetime.now() + datetime.timedelta(minutes=6)
            pickle.dump(the_medium_term_future.timestamp(), open("tests/cassettes_special/test_scheduled_status_long_datetimeobjects.pkl", 'wb'))
        scheduled_toot = api.status_post(f"please ensure maximum headroom at {the_medium_term_future}", scheduled_at=the_medium_term_future)
        scheduled_toot_list = api.scheduled_statuses()
        assert any(x.id == scheduled_toot.id for x in scheduled_toot_list)
        pickle.dump(scheduled_toot.params.text, open("tests/cassettes_special/test_scheduled_status_long_text.pkl", 'wb'))

@pytest.mark.vcr(match_on=['path'])    
def test_scheduled_status_long_part2(api):
        with vcr.use_cassette('test_scheduled_status_long_part2.yaml', cassette_library_dir='tests/cassettes_special', record_mode='once'):
            text = pickle.load(open("tests/cassettes_special/test_scheduled_status_long_text.pkl", 'rb'))
            statuses = api.timeline_home()
            print(text)
            found_status = False
            for status in statuses:
                if text in status.content:
                    found_status = True
            assert found_status

@pytest.mark.vcr()
def test_status_edit(api, api2):
    status = api.status_post("the best editor? why, of course it is VS Code")
    edit_list_1 = api2.status_history(status)
    status_edited = api.status_update(status, "the best editor? why, of course it is the KDE Advanced Text Editor, Kate")
    status_result = api2.status(status)
    edit_list_2 = api2.status_history(status)

    assert len(edit_list_1) == 0
    assert len(edit_list_2) == 2
    assert "the best editor? why, of course it is the KDE Advanced Text Editor, Kate" in status_result.content

    source = api2.status_source(status)
    assert source.text == "the best editor? why, of course it is the KDE Advanced Text Editor, Kate"
    