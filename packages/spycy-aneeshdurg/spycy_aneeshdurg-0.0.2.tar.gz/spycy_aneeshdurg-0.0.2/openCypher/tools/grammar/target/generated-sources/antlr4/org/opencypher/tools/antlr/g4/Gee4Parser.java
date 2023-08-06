// Generated from org/opencypher/tools/antlr/g4/Gee4.g4 by ANTLR 4.7.2
package org.opencypher.tools.antlr.g4;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class Gee4Parser extends Parser {
	static { RuntimeMetaData.checkVersion("4.7.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, QUOTED_STRING=8, 
		NEGATED_STRING=9, CHAR_SET=10, NEGATED_CHAR_SET=11, DOT_PATTERN=12, IDENTIFIER=13, 
		OR=14, QUESTION=15, PLUS=16, STAR=17, ACTION=18, QUASI_COMMENT=19, NORMAL_LINE_COMMENT=20, 
		SINGLE_LINE_COMMENT=21, MULTILINE_COMMENT=22, WS=23;
	public static final int
		RULE_wholegrammar = 0, RULE_header = 1, RULE_grammardef = 2, RULE_rulelist = 3, 
		RULE_rule_ = 4, RULE_description = 5, RULE_ruleName = 6, RULE_ruleElements = 7, 
		RULE_ruleAlternative = 8, RULE_ruleItem = 9, RULE_ruleComponent = 10, 
		RULE_cardinality = 11, RULE_literal = 12, RULE_quotedString = 13, RULE_negatedQuotedString = 14, 
		RULE_charSet = 15, RULE_negatedCharSet = 16, RULE_dotPattern = 17, RULE_ruleReference = 18, 
		RULE_specialRule = 19, RULE_fragmentRule = 20;
	private static String[] makeRuleNames() {
		return new String[] {
			"wholegrammar", "header", "grammardef", "rulelist", "rule_", "description", 
			"ruleName", "ruleElements", "ruleAlternative", "ruleItem", "ruleComponent", 
			"cardinality", "literal", "quotedString", "negatedQuotedString", "charSet", 
			"negatedCharSet", "dotPattern", "ruleReference", "specialRule", "fragmentRule"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'grammar'", "';'", "':'", "'('", "')'", "'->'", "'fragment'", 
			null, null, null, null, null, null, "'|'", "'?'", "'+'", "'*'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, "QUOTED_STRING", "NEGATED_STRING", 
			"CHAR_SET", "NEGATED_CHAR_SET", "DOT_PATTERN", "IDENTIFIER", "OR", "QUESTION", 
			"PLUS", "STAR", "ACTION", "QUASI_COMMENT", "NORMAL_LINE_COMMENT", "SINGLE_LINE_COMMENT", 
			"MULTILINE_COMMENT", "WS"
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
	public String getGrammarFileName() { return "Gee4.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public Gee4Parser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class WholegrammarContext extends ParserRuleContext {
		public GrammardefContext grammardef() {
			return getRuleContext(GrammardefContext.class,0);
		}
		public RulelistContext rulelist() {
			return getRuleContext(RulelistContext.class,0);
		}
		public HeaderContext header() {
			return getRuleContext(HeaderContext.class,0);
		}
		public WholegrammarContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_wholegrammar; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterWholegrammar(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitWholegrammar(this);
		}
	}

	public final WholegrammarContext wholegrammar() throws RecognitionException {
		WholegrammarContext _localctx = new WholegrammarContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_wholegrammar);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(43);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==QUASI_COMMENT) {
				{
				setState(42);
				header();
				}
			}

			setState(45);
			grammardef();
			setState(46);
			rulelist();
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

	public static class HeaderContext extends ParserRuleContext {
		public TerminalNode QUASI_COMMENT() { return getToken(Gee4Parser.QUASI_COMMENT, 0); }
		public HeaderContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_header; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterHeader(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitHeader(this);
		}
	}

	public final HeaderContext header() throws RecognitionException {
		HeaderContext _localctx = new HeaderContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_header);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(48);
			match(QUASI_COMMENT);
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

	public static class GrammardefContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(Gee4Parser.IDENTIFIER, 0); }
		public GrammardefContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grammardef; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterGrammardef(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitGrammardef(this);
		}
	}

	public final GrammardefContext grammardef() throws RecognitionException {
		GrammardefContext _localctx = new GrammardefContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_grammardef);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(50);
			match(T__0);
			setState(51);
			match(IDENTIFIER);
			setState(52);
			match(T__1);
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

	public static class RulelistContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(Gee4Parser.EOF, 0); }
		public List<Rule_Context> rule_() {
			return getRuleContexts(Rule_Context.class);
		}
		public Rule_Context rule_(int i) {
			return getRuleContext(Rule_Context.class,i);
		}
		public List<SpecialRuleContext> specialRule() {
			return getRuleContexts(SpecialRuleContext.class);
		}
		public SpecialRuleContext specialRule(int i) {
			return getRuleContext(SpecialRuleContext.class,i);
		}
		public List<FragmentRuleContext> fragmentRule() {
			return getRuleContexts(FragmentRuleContext.class);
		}
		public FragmentRuleContext fragmentRule(int i) {
			return getRuleContext(FragmentRuleContext.class,i);
		}
		public RulelistContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rulelist; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterRulelist(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitRulelist(this);
		}
	}

	public final RulelistContext rulelist() throws RecognitionException {
		RulelistContext _localctx = new RulelistContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_rulelist);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(59);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__6) | (1L << IDENTIFIER) | (1L << QUASI_COMMENT))) != 0)) {
				{
				setState(57);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,1,_ctx) ) {
				case 1:
					{
					setState(54);
					rule_();
					}
					break;
				case 2:
					{
					setState(55);
					specialRule();
					}
					break;
				case 3:
					{
					setState(56);
					fragmentRule();
					}
					break;
				}
				}
				setState(61);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(62);
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

	public static class Rule_Context extends ParserRuleContext {
		public RuleNameContext ruleName() {
			return getRuleContext(RuleNameContext.class,0);
		}
		public RuleElementsContext ruleElements() {
			return getRuleContext(RuleElementsContext.class,0);
		}
		public DescriptionContext description() {
			return getRuleContext(DescriptionContext.class,0);
		}
		public Rule_Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rule_; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterRule_(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitRule_(this);
		}
	}

	public final Rule_Context rule_() throws RecognitionException {
		Rule_Context _localctx = new Rule_Context(_ctx, getState());
		enterRule(_localctx, 8, RULE_rule_);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(65);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==QUASI_COMMENT) {
				{
				setState(64);
				description();
				}
			}

			setState(67);
			ruleName();
			setState(68);
			match(T__2);
			setState(69);
			ruleElements();
			setState(70);
			match(T__1);
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

	public static class DescriptionContext extends ParserRuleContext {
		public TerminalNode QUASI_COMMENT() { return getToken(Gee4Parser.QUASI_COMMENT, 0); }
		public DescriptionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_description; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterDescription(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitDescription(this);
		}
	}

	public final DescriptionContext description() throws RecognitionException {
		DescriptionContext _localctx = new DescriptionContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_description);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(72);
			match(QUASI_COMMENT);
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

	public static class RuleNameContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(Gee4Parser.IDENTIFIER, 0); }
		public RuleNameContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ruleName; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterRuleName(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitRuleName(this);
		}
	}

	public final RuleNameContext ruleName() throws RecognitionException {
		RuleNameContext _localctx = new RuleNameContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_ruleName);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(74);
			match(IDENTIFIER);
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

	public static class RuleElementsContext extends ParserRuleContext {
		public List<RuleAlternativeContext> ruleAlternative() {
			return getRuleContexts(RuleAlternativeContext.class);
		}
		public RuleAlternativeContext ruleAlternative(int i) {
			return getRuleContext(RuleAlternativeContext.class,i);
		}
		public List<TerminalNode> OR() { return getTokens(Gee4Parser.OR); }
		public TerminalNode OR(int i) {
			return getToken(Gee4Parser.OR, i);
		}
		public RuleElementsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ruleElements; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterRuleElements(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitRuleElements(this);
		}
	}

	public final RuleElementsContext ruleElements() throws RecognitionException {
		RuleElementsContext _localctx = new RuleElementsContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_ruleElements);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(76);
			ruleAlternative();
			setState(81);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==OR) {
				{
				{
				setState(77);
				match(OR);
				setState(78);
				ruleAlternative();
				}
				}
				setState(83);
				_errHandler.sync(this);
				_la = _input.LA(1);
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

	public static class RuleAlternativeContext extends ParserRuleContext {
		public List<RuleItemContext> ruleItem() {
			return getRuleContexts(RuleItemContext.class);
		}
		public RuleItemContext ruleItem(int i) {
			return getRuleContext(RuleItemContext.class,i);
		}
		public RuleAlternativeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ruleAlternative; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterRuleAlternative(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitRuleAlternative(this);
		}
	}

	public final RuleAlternativeContext ruleAlternative() throws RecognitionException {
		RuleAlternativeContext _localctx = new RuleAlternativeContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_ruleAlternative);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(87);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__3) | (1L << QUOTED_STRING) | (1L << NEGATED_STRING) | (1L << CHAR_SET) | (1L << NEGATED_CHAR_SET) | (1L << DOT_PATTERN) | (1L << IDENTIFIER))) != 0)) {
				{
				{
				setState(84);
				ruleItem();
				}
				}
				setState(89);
				_errHandler.sync(this);
				_la = _input.LA(1);
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

	public static class RuleItemContext extends ParserRuleContext {
		public RuleComponentContext ruleComponent() {
			return getRuleContext(RuleComponentContext.class,0);
		}
		public RuleElementsContext ruleElements() {
			return getRuleContext(RuleElementsContext.class,0);
		}
		public CardinalityContext cardinality() {
			return getRuleContext(CardinalityContext.class,0);
		}
		public RuleItemContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ruleItem; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterRuleItem(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitRuleItem(this);
		}
	}

	public final RuleItemContext ruleItem() throws RecognitionException {
		RuleItemContext _localctx = new RuleItemContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_ruleItem);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(95);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case QUOTED_STRING:
			case NEGATED_STRING:
			case CHAR_SET:
			case NEGATED_CHAR_SET:
			case DOT_PATTERN:
			case IDENTIFIER:
				{
				setState(90);
				ruleComponent();
				}
				break;
			case T__3:
				{
				setState(91);
				match(T__3);
				setState(92);
				ruleElements();
				setState(93);
				match(T__4);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			setState(98);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << QUESTION) | (1L << PLUS) | (1L << STAR))) != 0)) {
				{
				setState(97);
				cardinality();
				}
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

	public static class RuleComponentContext extends ParserRuleContext {
		public RuleReferenceContext ruleReference() {
			return getRuleContext(RuleReferenceContext.class,0);
		}
		public LiteralContext literal() {
			return getRuleContext(LiteralContext.class,0);
		}
		public RuleComponentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ruleComponent; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterRuleComponent(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitRuleComponent(this);
		}
	}

	public final RuleComponentContext ruleComponent() throws RecognitionException {
		RuleComponentContext _localctx = new RuleComponentContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_ruleComponent);
		try {
			setState(102);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case IDENTIFIER:
				enterOuterAlt(_localctx, 1);
				{
				setState(100);
				ruleReference();
				}
				break;
			case QUOTED_STRING:
			case NEGATED_STRING:
			case CHAR_SET:
			case NEGATED_CHAR_SET:
			case DOT_PATTERN:
				enterOuterAlt(_localctx, 2);
				{
				setState(101);
				literal();
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

	public static class CardinalityContext extends ParserRuleContext {
		public TerminalNode QUESTION() { return getToken(Gee4Parser.QUESTION, 0); }
		public TerminalNode PLUS() { return getToken(Gee4Parser.PLUS, 0); }
		public TerminalNode STAR() { return getToken(Gee4Parser.STAR, 0); }
		public CardinalityContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cardinality; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterCardinality(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitCardinality(this);
		}
	}

	public final CardinalityContext cardinality() throws RecognitionException {
		CardinalityContext _localctx = new CardinalityContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_cardinality);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(104);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << QUESTION) | (1L << PLUS) | (1L << STAR))) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
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

	public static class LiteralContext extends ParserRuleContext {
		public QuotedStringContext quotedString() {
			return getRuleContext(QuotedStringContext.class,0);
		}
		public NegatedQuotedStringContext negatedQuotedString() {
			return getRuleContext(NegatedQuotedStringContext.class,0);
		}
		public CharSetContext charSet() {
			return getRuleContext(CharSetContext.class,0);
		}
		public NegatedCharSetContext negatedCharSet() {
			return getRuleContext(NegatedCharSetContext.class,0);
		}
		public DotPatternContext dotPattern() {
			return getRuleContext(DotPatternContext.class,0);
		}
		public LiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_literal; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitLiteral(this);
		}
	}

	public final LiteralContext literal() throws RecognitionException {
		LiteralContext _localctx = new LiteralContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_literal);
		try {
			setState(111);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case QUOTED_STRING:
				enterOuterAlt(_localctx, 1);
				{
				setState(106);
				quotedString();
				}
				break;
			case NEGATED_STRING:
				enterOuterAlt(_localctx, 2);
				{
				setState(107);
				negatedQuotedString();
				}
				break;
			case CHAR_SET:
				enterOuterAlt(_localctx, 3);
				{
				setState(108);
				charSet();
				}
				break;
			case NEGATED_CHAR_SET:
				enterOuterAlt(_localctx, 4);
				{
				setState(109);
				negatedCharSet();
				}
				break;
			case DOT_PATTERN:
				enterOuterAlt(_localctx, 5);
				{
				setState(110);
				dotPattern();
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

	public static class QuotedStringContext extends ParserRuleContext {
		public TerminalNode QUOTED_STRING() { return getToken(Gee4Parser.QUOTED_STRING, 0); }
		public QuotedStringContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_quotedString; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterQuotedString(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitQuotedString(this);
		}
	}

	public final QuotedStringContext quotedString() throws RecognitionException {
		QuotedStringContext _localctx = new QuotedStringContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_quotedString);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(113);
			match(QUOTED_STRING);
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

	public static class NegatedQuotedStringContext extends ParserRuleContext {
		public TerminalNode NEGATED_STRING() { return getToken(Gee4Parser.NEGATED_STRING, 0); }
		public NegatedQuotedStringContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_negatedQuotedString; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterNegatedQuotedString(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitNegatedQuotedString(this);
		}
	}

	public final NegatedQuotedStringContext negatedQuotedString() throws RecognitionException {
		NegatedQuotedStringContext _localctx = new NegatedQuotedStringContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_negatedQuotedString);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(115);
			match(NEGATED_STRING);
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

	public static class CharSetContext extends ParserRuleContext {
		public TerminalNode CHAR_SET() { return getToken(Gee4Parser.CHAR_SET, 0); }
		public CharSetContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_charSet; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterCharSet(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitCharSet(this);
		}
	}

	public final CharSetContext charSet() throws RecognitionException {
		CharSetContext _localctx = new CharSetContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_charSet);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(117);
			match(CHAR_SET);
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

	public static class NegatedCharSetContext extends ParserRuleContext {
		public TerminalNode NEGATED_CHAR_SET() { return getToken(Gee4Parser.NEGATED_CHAR_SET, 0); }
		public NegatedCharSetContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_negatedCharSet; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterNegatedCharSet(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitNegatedCharSet(this);
		}
	}

	public final NegatedCharSetContext negatedCharSet() throws RecognitionException {
		NegatedCharSetContext _localctx = new NegatedCharSetContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_negatedCharSet);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(119);
			match(NEGATED_CHAR_SET);
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

	public static class DotPatternContext extends ParserRuleContext {
		public TerminalNode DOT_PATTERN() { return getToken(Gee4Parser.DOT_PATTERN, 0); }
		public DotPatternContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_dotPattern; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterDotPattern(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitDotPattern(this);
		}
	}

	public final DotPatternContext dotPattern() throws RecognitionException {
		DotPatternContext _localctx = new DotPatternContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_dotPattern);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(121);
			match(DOT_PATTERN);
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

	public static class RuleReferenceContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(Gee4Parser.IDENTIFIER, 0); }
		public RuleReferenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ruleReference; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterRuleReference(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitRuleReference(this);
		}
	}

	public final RuleReferenceContext ruleReference() throws RecognitionException {
		RuleReferenceContext _localctx = new RuleReferenceContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_ruleReference);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(123);
			match(IDENTIFIER);
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

	public static class SpecialRuleContext extends ParserRuleContext {
		public RuleNameContext ruleName() {
			return getRuleContext(RuleNameContext.class,0);
		}
		public List<TerminalNode> IDENTIFIER() { return getTokens(Gee4Parser.IDENTIFIER); }
		public TerminalNode IDENTIFIER(int i) {
			return getToken(Gee4Parser.IDENTIFIER, i);
		}
		public TerminalNode ACTION() { return getToken(Gee4Parser.ACTION, 0); }
		public RuleElementsContext ruleElements() {
			return getRuleContext(RuleElementsContext.class,0);
		}
		public SpecialRuleContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_specialRule; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterSpecialRule(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitSpecialRule(this);
		}
	}

	public final SpecialRuleContext specialRule() throws RecognitionException {
		SpecialRuleContext _localctx = new SpecialRuleContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_specialRule);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(125);
			ruleName();
			setState(126);
			match(T__2);
			setState(137);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,11,_ctx) ) {
			case 1:
				{
				{
				setState(127);
				match(IDENTIFIER);
				setState(128);
				match(ACTION);
				}
				}
				break;
			case 2:
				{
				{
				setState(129);
				ruleElements();
				setState(130);
				match(T__5);
				setState(131);
				match(IDENTIFIER);
				setState(135);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__3) {
					{
					setState(132);
					match(T__3);
					setState(133);
					match(IDENTIFIER);
					setState(134);
					match(T__4);
					}
				}

				}
				}
				break;
			}
			setState(139);
			match(T__1);
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

	public static class FragmentRuleContext extends ParserRuleContext {
		public RuleNameContext ruleName() {
			return getRuleContext(RuleNameContext.class,0);
		}
		public LiteralContext literal() {
			return getRuleContext(LiteralContext.class,0);
		}
		public FragmentRuleContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_fragmentRule; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).enterFragmentRule(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof Gee4Listener ) ((Gee4Listener)listener).exitFragmentRule(this);
		}
	}

	public final FragmentRuleContext fragmentRule() throws RecognitionException {
		FragmentRuleContext _localctx = new FragmentRuleContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_fragmentRule);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(141);
			match(T__6);
			setState(142);
			ruleName();
			setState(143);
			match(T__2);
			setState(144);
			literal();
			setState(145);
			match(T__1);
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
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\31\u0096\4\2\t\2"+
		"\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\3\2\5\2.\n\2\3\2\3\2\3\2\3\3"+
		"\3\3\3\4\3\4\3\4\3\4\3\5\3\5\3\5\7\5<\n\5\f\5\16\5?\13\5\3\5\3\5\3\6\5"+
		"\6D\n\6\3\6\3\6\3\6\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\t\7\tR\n\t\f\t\16"+
		"\tU\13\t\3\n\7\nX\n\n\f\n\16\n[\13\n\3\13\3\13\3\13\3\13\3\13\5\13b\n"+
		"\13\3\13\5\13e\n\13\3\f\3\f\5\fi\n\f\3\r\3\r\3\16\3\16\3\16\3\16\3\16"+
		"\5\16r\n\16\3\17\3\17\3\20\3\20\3\21\3\21\3\22\3\22\3\23\3\23\3\24\3\24"+
		"\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\5\25\u008a\n\25\5\25"+
		"\u008c\n\25\3\25\3\25\3\26\3\26\3\26\3\26\3\26\3\26\3\26\2\2\27\2\4\6"+
		"\b\n\f\16\20\22\24\26\30\32\34\36 \"$&(*\2\3\3\2\21\23\2\u0090\2-\3\2"+
		"\2\2\4\62\3\2\2\2\6\64\3\2\2\2\b=\3\2\2\2\nC\3\2\2\2\fJ\3\2\2\2\16L\3"+
		"\2\2\2\20N\3\2\2\2\22Y\3\2\2\2\24a\3\2\2\2\26h\3\2\2\2\30j\3\2\2\2\32"+
		"q\3\2\2\2\34s\3\2\2\2\36u\3\2\2\2 w\3\2\2\2\"y\3\2\2\2${\3\2\2\2&}\3\2"+
		"\2\2(\177\3\2\2\2*\u008f\3\2\2\2,.\5\4\3\2-,\3\2\2\2-.\3\2\2\2./\3\2\2"+
		"\2/\60\5\6\4\2\60\61\5\b\5\2\61\3\3\2\2\2\62\63\7\25\2\2\63\5\3\2\2\2"+
		"\64\65\7\3\2\2\65\66\7\17\2\2\66\67\7\4\2\2\67\7\3\2\2\28<\5\n\6\29<\5"+
		"(\25\2:<\5*\26\2;8\3\2\2\2;9\3\2\2\2;:\3\2\2\2<?\3\2\2\2=;\3\2\2\2=>\3"+
		"\2\2\2>@\3\2\2\2?=\3\2\2\2@A\7\2\2\3A\t\3\2\2\2BD\5\f\7\2CB\3\2\2\2CD"+
		"\3\2\2\2DE\3\2\2\2EF\5\16\b\2FG\7\5\2\2GH\5\20\t\2HI\7\4\2\2I\13\3\2\2"+
		"\2JK\7\25\2\2K\r\3\2\2\2LM\7\17\2\2M\17\3\2\2\2NS\5\22\n\2OP\7\20\2\2"+
		"PR\5\22\n\2QO\3\2\2\2RU\3\2\2\2SQ\3\2\2\2ST\3\2\2\2T\21\3\2\2\2US\3\2"+
		"\2\2VX\5\24\13\2WV\3\2\2\2X[\3\2\2\2YW\3\2\2\2YZ\3\2\2\2Z\23\3\2\2\2["+
		"Y\3\2\2\2\\b\5\26\f\2]^\7\6\2\2^_\5\20\t\2_`\7\7\2\2`b\3\2\2\2a\\\3\2"+
		"\2\2a]\3\2\2\2bd\3\2\2\2ce\5\30\r\2dc\3\2\2\2de\3\2\2\2e\25\3\2\2\2fi"+
		"\5&\24\2gi\5\32\16\2hf\3\2\2\2hg\3\2\2\2i\27\3\2\2\2jk\t\2\2\2k\31\3\2"+
		"\2\2lr\5\34\17\2mr\5\36\20\2nr\5 \21\2or\5\"\22\2pr\5$\23\2ql\3\2\2\2"+
		"qm\3\2\2\2qn\3\2\2\2qo\3\2\2\2qp\3\2\2\2r\33\3\2\2\2st\7\n\2\2t\35\3\2"+
		"\2\2uv\7\13\2\2v\37\3\2\2\2wx\7\f\2\2x!\3\2\2\2yz\7\r\2\2z#\3\2\2\2{|"+
		"\7\16\2\2|%\3\2\2\2}~\7\17\2\2~\'\3\2\2\2\177\u0080\5\16\b\2\u0080\u008b"+
		"\7\5\2\2\u0081\u0082\7\17\2\2\u0082\u008c\7\24\2\2\u0083\u0084\5\20\t"+
		"\2\u0084\u0085\7\b\2\2\u0085\u0089\7\17\2\2\u0086\u0087\7\6\2\2\u0087"+
		"\u0088\7\17\2\2\u0088\u008a\7\7\2\2\u0089\u0086\3\2\2\2\u0089\u008a\3"+
		"\2\2\2\u008a\u008c\3\2\2\2\u008b\u0081\3\2\2\2\u008b\u0083\3\2\2\2\u008c"+
		"\u008d\3\2\2\2\u008d\u008e\7\4\2\2\u008e)\3\2\2\2\u008f\u0090\7\t\2\2"+
		"\u0090\u0091\5\16\b\2\u0091\u0092\7\5\2\2\u0092\u0093\5\32\16\2\u0093"+
		"\u0094\7\4\2\2\u0094+\3\2\2\2\16-;=CSYadhq\u0089\u008b";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}