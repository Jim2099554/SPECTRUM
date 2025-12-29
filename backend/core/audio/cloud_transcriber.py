from typing import List, Dict, Any, Callable, Optional
from datetime import datetime
from collections import defaultdict
from google.cloud import speech
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertSystem:
    def __init__(self):
        self.alert_rules = []
        self.alert_handlers = []
        self.alert_history = defaultdict(list)

    def add_rule(self, rule: Dict[str, Any]):
        self.alert_rules.append(rule)

    def add_alert_handler(self, handler: Callable):
        self.alert_handlers.append(handler)

    async def process_content(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        generated_alerts = []

        for rule in self.alert_rules:
            if await self._check_rule_conditions(rule, content):
                alert = self._create_alert(rule, content)

                if self._check_cooldown(rule, alert) and not self._is_duplicate_alert(rule, alert):
                    generated_alerts.append(alert)
                    self.alert_history[rule["name"]].append(alert)
                    await self._notify_handlers(alert)

        return generated_alerts

    async def _check_rule_conditions(self, rule: Dict[str, Any], content: Dict[str, Any]) -> bool:
        for condition in rule["conditions"]:
            condition_type = condition["type"]

            if condition_type == "keyword":
                if not any(kw in content.get("keywords", []) for kw in condition["keywords"]):
                    return False
            elif condition_type == "pattern":
                if not any(p["pattern_name"] == condition["pattern_name"] for p in content.get("pattern_matches", [])):
                    return False
            elif condition_type == "sentiment":
                sentiment = content.get("sentiment", {}).get("label")
                if sentiment != condition["sentiment"]:
                    return False
        return True

    def _create_alert(self, rule: Dict[str, Any], content: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "rule_name": rule["name"],
            "severity": rule["severity"],
            "timestamp": datetime.utcnow().isoformat(),
            "content_summary": content.get("summary", ""),
            "matched_conditions": rule["conditions"]
        }

    def _check_cooldown(self, rule: Dict[str, Any], alert: Dict[str, Any]) -> bool:
        if not self.alert_history[rule["name"]]:
            return True

        last_alert = self.alert_history[rule["name"]][-1]
        last_time = datetime.fromisoformat(last_alert["timestamp"])
        current_time = datetime.fromisoformat(alert["timestamp"])

        cooldown_minutes = rule.get("cooldown", 0)
        time_diff = (current_time - last_time).total_seconds() / 60

        return time_diff >= cooldown_minutes

    def _is_duplicate_alert(self, rule: Dict[str, Any], alert: Dict[str, Any]) -> bool:
        recent_alerts = self.alert_history[rule["name"]][-5:]
        for previous_alert in recent_alerts:
            if alert["content_summary"] == previous_alert["content_summary"]:
                return True
        return False

    async def _notify_handlers(self, alert: Dict[str, Any]):
        for handler in self.alert_handlers:
            try:
                await handler(alert)
            except Exception as e:
                logger.error(f"Error in alert handler: {str(e)}")


def transcribe_gcs(gcs_uri: str, enable_speaker_diarization: bool = True, diarization_speaker_count: int = 2,
                   language_code: str = "en-US", sample_rate_hertz: int = 16000,
                   model: str = "latest_long", timeout: int = 600,
                   alert_keywords: Optional[List[str]] = None,
                   audio_base_url: Optional[str] = None) -> Optional[list]:
    """
    Transcribe an audio file stored in Google Cloud Storage and organize by speaker.
    Includes enriched data for frontend UI display (chat bubbles, alert highlights, audio buttons).
    """
    try:
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
            enable_speaker_diarization=enable_speaker_diarization,
            diarization_speaker_count=diarization_speaker_count,
            model=model
        )

        operation = client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=timeout)
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        return None

    segments = []
    current_speaker = None
    current_words = []
    start_time = None

    for result in response.results:
        alternative = result.alternatives[0]
        for word_info in alternative.words:
            speaker = word_info.speaker_tag
            if speaker != current_speaker:
                if current_speaker is not None and current_words:
                    segment_text = " ".join([w["word"] for w in current_words])
                    alert_hit = any(kw.lower() in segment_text.lower() for kw in (alert_keywords or []))
                    segments.append({
                        "speaker": current_speaker,
                        "start": start_time,
                        "end": current_words[-1]["end"],
                        "transcript": segment_text,
                        "alert": alert_hit,
                        "audio_url": f"{audio_base_url}?start={start_time:.2f}&end={current_words[-1]['end']:.2f}" if audio_base_url else None
                    })
                current_words = []
                current_speaker = speaker
                start_time = word_info.start_time.total_seconds()

            current_words.append({
                "word": word_info.word,
                "start": word_info.start_time.total_seconds(),
                "end": word_info.end_time.total_seconds()
            })

    if current_words:
        segment_text = " ".join([w["word"] for w in current_words])
        alert_hit = any(kw.lower() in segment_text.lower() for kw in (alert_keywords or []))
        segments.append({
            "speaker": current_speaker,
            "start": start_time,
            "end": current_words[-1]["end"],
            "transcript": segment_text,
            "alert": alert_hit,
            "audio_url": f"{audio_base_url}?start={start_time:.2f}&end={current_words[-1]['end']:.2f}" if audio_base_url else None
        })

    return segments