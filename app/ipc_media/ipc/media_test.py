
import unittest
from ipc.media import Media
from fs.util import get_ipc_events


class MockedClient():
  def send(self, msg):
    return True


class TestingMedia(unittest.TestCase):
  def test_format_msg(self):
    formatted = Media.format_msg('test-event', 'test-payload')
    self.assertDictEqual(
        formatted, {'data': {'payload': 'test-payload'},
                    'type': 'test-event'})

  @staticmethod
  def generateMedia():
    media = Media(1)
    media.ipc_events = get_ipc_events()
    return media

  def test_motion_detected(self):
    media = TestingMedia.generateMedia()
    media.motion_detected('no/such/file', -1)
    self.assertEqual(media.OUTGOING_MESSAGES, [
        {'type': 'rp-cam.motion-detected', 'data':
         {'payload': {'path': 'no/such/file', 'score': -1}}}])
    media.process_incoming()
    self.assertCountEqual(media.INCOMING_MESSAGES, [])

  def test_outgoing_messages(self):
    media = TestingMedia.generateMedia()
    media.add_message('test-event-1', 'test-payload-2')
    self.assertEqual(media.OUTGOING_MESSAGES, [
                     {'type': 'test-event-1', 'data': {'payload': 'test-payload-2'}}])
    media.add_message('test-event-2', 'test-payload-2')
    self.assertEqual(len(media.OUTGOING_MESSAGES), 2)
    media.dispatch_outstanding(MockedClient())
    self.assertCountEqual(media.OUTGOING_MESSAGES, [])
    self.assertEqual(media._outgoing_messages_lock.locked(), False)

  def test_incoming_messages(self):
    media = TestingMedia.generateMedia()
    media.accept_event(Media.format_msg('test-event-3', 'test-payload-3'))
    self.assertEqual(media.INCOMING_MESSAGES, [
                     {'type': 'test-event-3', 'data': {'payload': 'test-payload-3'}}])
    media.accept_event(Media.format_msg('test-event-4', 'test-payload-4'))
    self.assertEqual(len(media.INCOMING_MESSAGES), 2)
    media.process_incoming()
    self.assertCountEqual(media.INCOMING_MESSAGES, [])
    self.assertEqual(media._incoming_messages_lock.locked(), False)
