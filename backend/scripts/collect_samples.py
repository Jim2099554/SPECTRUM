import os
import argparse
from core.analysis.voice_analyzer import VoiceAnalyzer

parser = argparse.ArgumentParser(description='Enroll new speakers')
parser.add_argument('--user', required=True, help='User ID to enroll')
parser.add_argument('--samples', nargs='+', required=True, help='Audio sample paths')
args = parser.parse_args()

analyzer = VoiceAnalyzer()
analyzer.enroll_speaker(args.user, args.samples)
print(f'Enrolled {args.user} with {len(args.samples)} samples')
