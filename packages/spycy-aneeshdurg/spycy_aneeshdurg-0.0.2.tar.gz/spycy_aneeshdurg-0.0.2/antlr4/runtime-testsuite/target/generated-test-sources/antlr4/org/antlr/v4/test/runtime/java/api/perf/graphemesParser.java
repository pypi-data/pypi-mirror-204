// Generated from org/antlr/v4/test/runtime/java/api/perf/graphemes.g4 by ANTLR 4.12.0
package org.antlr.v4.test.runtime.java.api.perf;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class graphemesParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.12.0", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		Extend=1, ZWJ=2, SpacingMark=3, EmojiCoreSequence=4, EmojiZWJSequence=5, 
		Prepend=6, NonControl=7, CRLF=8, HangulSyllable=9;
	public static final int
		RULE_emoji_sequence = 0, RULE_grapheme_cluster = 1, RULE_graphemes = 2;
	private static String[] makeRuleNames() {
		return new String[] {
			"emoji_sequence", "grapheme_cluster", "graphemes"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, null, "'\\u200D'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "Extend", "ZWJ", "SpacingMark", "EmojiCoreSequence", "EmojiZWJSequence", 
			"Prepend", "NonControl", "CRLF", "HangulSyllable"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "graphemes.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public graphemesParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Emoji_sequenceContext extends ParserRuleContext {
		public TerminalNode EmojiZWJSequence() { return getToken(graphemesParser.EmojiZWJSequence, 0); }
		public TerminalNode EmojiCoreSequence() { return getToken(graphemesParser.EmojiCoreSequence, 0); }
		public List<TerminalNode> Extend() { return getTokens(graphemesParser.Extend); }
		public TerminalNode Extend(int i) {
			return getToken(graphemesParser.Extend, i);
		}
		public List<TerminalNode> ZWJ() { return getTokens(graphemesParser.ZWJ); }
		public TerminalNode ZWJ(int i) {
			return getToken(graphemesParser.ZWJ, i);
		}
		public List<TerminalNode> SpacingMark() { return getTokens(graphemesParser.SpacingMark); }
		public TerminalNode SpacingMark(int i) {
			return getToken(graphemesParser.SpacingMark, i);
		}
		public Emoji_sequenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_emoji_sequence; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof graphemesListener ) ((graphemesListener)listener).enterEmoji_sequence(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof graphemesListener ) ((graphemesListener)listener).exitEmoji_sequence(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof graphemesVisitor ) return ((graphemesVisitor<? extends T>)visitor).visitEmoji_sequence(this);
			else return visitor.visitChildren(this);
		}
	}

	public final Emoji_sequenceContext emoji_sequence() throws RecognitionException {
		Emoji_sequenceContext _localctx = new Emoji_sequenceContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_emoji_sequence);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(6);
			_la = _input.LA(1);
			if ( !(_la==EmojiCoreSequence || _la==EmojiZWJSequence) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			setState(10);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,0,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(7);
					_la = _input.LA(1);
					if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 14L) != 0)) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					}
					} 
				}
				setState(12);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,0,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Grapheme_clusterContext extends ParserRuleContext {
		public TerminalNode CRLF() { return getToken(graphemesParser.CRLF, 0); }
		public Emoji_sequenceContext emoji_sequence() {
			return getRuleContext(Emoji_sequenceContext.class,0);
		}
		public TerminalNode HangulSyllable() { return getToken(graphemesParser.HangulSyllable, 0); }
		public TerminalNode NonControl() { return getToken(graphemesParser.NonControl, 0); }
		public List<TerminalNode> Prepend() { return getTokens(graphemesParser.Prepend); }
		public TerminalNode Prepend(int i) {
			return getToken(graphemesParser.Prepend, i);
		}
		public List<TerminalNode> Extend() { return getTokens(graphemesParser.Extend); }
		public TerminalNode Extend(int i) {
			return getToken(graphemesParser.Extend, i);
		}
		public List<TerminalNode> ZWJ() { return getTokens(graphemesParser.ZWJ); }
		public TerminalNode ZWJ(int i) {
			return getToken(graphemesParser.ZWJ, i);
		}
		public List<TerminalNode> SpacingMark() { return getTokens(graphemesParser.SpacingMark); }
		public TerminalNode SpacingMark(int i) {
			return getToken(graphemesParser.SpacingMark, i);
		}
		public Grapheme_clusterContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grapheme_cluster; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof graphemesListener ) ((graphemesListener)listener).enterGrapheme_cluster(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof graphemesListener ) ((graphemesListener)listener).exitGrapheme_cluster(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof graphemesVisitor ) return ((graphemesVisitor<? extends T>)visitor).visitGrapheme_cluster(this);
			else return visitor.visitChildren(this);
		}
	}

	public final Grapheme_clusterContext grapheme_cluster() throws RecognitionException {
		Grapheme_clusterContext _localctx = new Grapheme_clusterContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_grapheme_cluster);
		int _la;
		try {
			setState(31);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case CRLF:
				enterOuterAlt(_localctx, 1);
				{
				setState(13);
				match(CRLF);
				}
				break;
			case EmojiCoreSequence:
			case EmojiZWJSequence:
			case Prepend:
			case NonControl:
			case HangulSyllable:
				enterOuterAlt(_localctx, 2);
				{
				setState(17);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==Prepend) {
					{
					{
					setState(14);
					match(Prepend);
					}
					}
					setState(19);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(23);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case EmojiCoreSequence:
				case EmojiZWJSequence:
					{
					setState(20);
					emoji_sequence();
					}
					break;
				case HangulSyllable:
					{
					setState(21);
					match(HangulSyllable);
					}
					break;
				case NonControl:
					{
					setState(22);
					match(NonControl);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(28);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 14L) != 0)) {
					{
					{
					setState(25);
					_la = _input.LA(1);
					if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 14L) != 0)) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					}
					}
					setState(30);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class GraphemesContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(graphemesParser.EOF, 0); }
		public List<Grapheme_clusterContext> grapheme_cluster() {
			return getRuleContexts(Grapheme_clusterContext.class);
		}
		public Grapheme_clusterContext grapheme_cluster(int i) {
			return getRuleContext(Grapheme_clusterContext.class,i);
		}
		public GraphemesContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_graphemes; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof graphemesListener ) ((graphemesListener)listener).enterGraphemes(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof graphemesListener ) ((graphemesListener)listener).exitGraphemes(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof graphemesVisitor ) return ((graphemesVisitor<? extends T>)visitor).visitGraphemes(this);
			else return visitor.visitChildren(this);
		}
	}

	public final GraphemesContext graphemes() throws RecognitionException {
		GraphemesContext _localctx = new GraphemesContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_graphemes);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(36);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 1008L) != 0)) {
				{
				{
				setState(33);
				grapheme_cluster();
				}
				}
				setState(38);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(39);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001\t*\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0001\u0000\u0001\u0000\u0005\u0000\t\b\u0000\n\u0000"+
		"\f\u0000\f\t\u0000\u0001\u0001\u0001\u0001\u0005\u0001\u0010\b\u0001\n"+
		"\u0001\f\u0001\u0013\t\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0003"+
		"\u0001\u0018\b\u0001\u0001\u0001\u0005\u0001\u001b\b\u0001\n\u0001\f\u0001"+
		"\u001e\t\u0001\u0003\u0001 \b\u0001\u0001\u0002\u0005\u0002#\b\u0002\n"+
		"\u0002\f\u0002&\t\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0000\u0000"+
		"\u0003\u0000\u0002\u0004\u0000\u0002\u0001\u0000\u0004\u0005\u0001\u0000"+
		"\u0001\u0003-\u0000\u0006\u0001\u0000\u0000\u0000\u0002\u001f\u0001\u0000"+
		"\u0000\u0000\u0004$\u0001\u0000\u0000\u0000\u0006\n\u0007\u0000\u0000"+
		"\u0000\u0007\t\u0007\u0001\u0000\u0000\b\u0007\u0001\u0000\u0000\u0000"+
		"\t\f\u0001\u0000\u0000\u0000\n\b\u0001\u0000\u0000\u0000\n\u000b\u0001"+
		"\u0000\u0000\u0000\u000b\u0001\u0001\u0000\u0000\u0000\f\n\u0001\u0000"+
		"\u0000\u0000\r \u0005\b\u0000\u0000\u000e\u0010\u0005\u0006\u0000\u0000"+
		"\u000f\u000e\u0001\u0000\u0000\u0000\u0010\u0013\u0001\u0000\u0000\u0000"+
		"\u0011\u000f\u0001\u0000\u0000\u0000\u0011\u0012\u0001\u0000\u0000\u0000"+
		"\u0012\u0017\u0001\u0000\u0000\u0000\u0013\u0011\u0001\u0000\u0000\u0000"+
		"\u0014\u0018\u0003\u0000\u0000\u0000\u0015\u0018\u0005\t\u0000\u0000\u0016"+
		"\u0018\u0005\u0007\u0000\u0000\u0017\u0014\u0001\u0000\u0000\u0000\u0017"+
		"\u0015\u0001\u0000\u0000\u0000\u0017\u0016\u0001\u0000\u0000\u0000\u0018"+
		"\u001c\u0001\u0000\u0000\u0000\u0019\u001b\u0007\u0001\u0000\u0000\u001a"+
		"\u0019\u0001\u0000\u0000\u0000\u001b\u001e\u0001\u0000\u0000\u0000\u001c"+
		"\u001a\u0001\u0000\u0000\u0000\u001c\u001d\u0001\u0000\u0000\u0000\u001d"+
		" \u0001\u0000\u0000\u0000\u001e\u001c\u0001\u0000\u0000\u0000\u001f\r"+
		"\u0001\u0000\u0000\u0000\u001f\u0011\u0001\u0000\u0000\u0000 \u0003\u0001"+
		"\u0000\u0000\u0000!#\u0003\u0002\u0001\u0000\"!\u0001\u0000\u0000\u0000"+
		"#&\u0001\u0000\u0000\u0000$\"\u0001\u0000\u0000\u0000$%\u0001\u0000\u0000"+
		"\u0000%\'\u0001\u0000\u0000\u0000&$\u0001\u0000\u0000\u0000\'(\u0005\u0000"+
		"\u0000\u0001(\u0005\u0001\u0000\u0000\u0000\u0006\n\u0011\u0017\u001c"+
		"\u001f$";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}