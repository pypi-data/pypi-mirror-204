// Generated from org/opencypher/tools/antlr/g4/Gee4.g4 by ANTLR 4.7.2
package org.opencypher.tools.antlr.g4;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link Gee4Parser}.
 */
public interface Gee4Listener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#wholegrammar}.
	 * @param ctx the parse tree
	 */
	void enterWholegrammar(Gee4Parser.WholegrammarContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#wholegrammar}.
	 * @param ctx the parse tree
	 */
	void exitWholegrammar(Gee4Parser.WholegrammarContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#header}.
	 * @param ctx the parse tree
	 */
	void enterHeader(Gee4Parser.HeaderContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#header}.
	 * @param ctx the parse tree
	 */
	void exitHeader(Gee4Parser.HeaderContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#grammardef}.
	 * @param ctx the parse tree
	 */
	void enterGrammardef(Gee4Parser.GrammardefContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#grammardef}.
	 * @param ctx the parse tree
	 */
	void exitGrammardef(Gee4Parser.GrammardefContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#rulelist}.
	 * @param ctx the parse tree
	 */
	void enterRulelist(Gee4Parser.RulelistContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#rulelist}.
	 * @param ctx the parse tree
	 */
	void exitRulelist(Gee4Parser.RulelistContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#rule_}.
	 * @param ctx the parse tree
	 */
	void enterRule_(Gee4Parser.Rule_Context ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#rule_}.
	 * @param ctx the parse tree
	 */
	void exitRule_(Gee4Parser.Rule_Context ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#description}.
	 * @param ctx the parse tree
	 */
	void enterDescription(Gee4Parser.DescriptionContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#description}.
	 * @param ctx the parse tree
	 */
	void exitDescription(Gee4Parser.DescriptionContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#ruleName}.
	 * @param ctx the parse tree
	 */
	void enterRuleName(Gee4Parser.RuleNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#ruleName}.
	 * @param ctx the parse tree
	 */
	void exitRuleName(Gee4Parser.RuleNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#ruleElements}.
	 * @param ctx the parse tree
	 */
	void enterRuleElements(Gee4Parser.RuleElementsContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#ruleElements}.
	 * @param ctx the parse tree
	 */
	void exitRuleElements(Gee4Parser.RuleElementsContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#ruleAlternative}.
	 * @param ctx the parse tree
	 */
	void enterRuleAlternative(Gee4Parser.RuleAlternativeContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#ruleAlternative}.
	 * @param ctx the parse tree
	 */
	void exitRuleAlternative(Gee4Parser.RuleAlternativeContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#ruleItem}.
	 * @param ctx the parse tree
	 */
	void enterRuleItem(Gee4Parser.RuleItemContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#ruleItem}.
	 * @param ctx the parse tree
	 */
	void exitRuleItem(Gee4Parser.RuleItemContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#ruleComponent}.
	 * @param ctx the parse tree
	 */
	void enterRuleComponent(Gee4Parser.RuleComponentContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#ruleComponent}.
	 * @param ctx the parse tree
	 */
	void exitRuleComponent(Gee4Parser.RuleComponentContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#cardinality}.
	 * @param ctx the parse tree
	 */
	void enterCardinality(Gee4Parser.CardinalityContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#cardinality}.
	 * @param ctx the parse tree
	 */
	void exitCardinality(Gee4Parser.CardinalityContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#literal}.
	 * @param ctx the parse tree
	 */
	void enterLiteral(Gee4Parser.LiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#literal}.
	 * @param ctx the parse tree
	 */
	void exitLiteral(Gee4Parser.LiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#quotedString}.
	 * @param ctx the parse tree
	 */
	void enterQuotedString(Gee4Parser.QuotedStringContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#quotedString}.
	 * @param ctx the parse tree
	 */
	void exitQuotedString(Gee4Parser.QuotedStringContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#negatedQuotedString}.
	 * @param ctx the parse tree
	 */
	void enterNegatedQuotedString(Gee4Parser.NegatedQuotedStringContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#negatedQuotedString}.
	 * @param ctx the parse tree
	 */
	void exitNegatedQuotedString(Gee4Parser.NegatedQuotedStringContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#charSet}.
	 * @param ctx the parse tree
	 */
	void enterCharSet(Gee4Parser.CharSetContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#charSet}.
	 * @param ctx the parse tree
	 */
	void exitCharSet(Gee4Parser.CharSetContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#negatedCharSet}.
	 * @param ctx the parse tree
	 */
	void enterNegatedCharSet(Gee4Parser.NegatedCharSetContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#negatedCharSet}.
	 * @param ctx the parse tree
	 */
	void exitNegatedCharSet(Gee4Parser.NegatedCharSetContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#dotPattern}.
	 * @param ctx the parse tree
	 */
	void enterDotPattern(Gee4Parser.DotPatternContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#dotPattern}.
	 * @param ctx the parse tree
	 */
	void exitDotPattern(Gee4Parser.DotPatternContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#ruleReference}.
	 * @param ctx the parse tree
	 */
	void enterRuleReference(Gee4Parser.RuleReferenceContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#ruleReference}.
	 * @param ctx the parse tree
	 */
	void exitRuleReference(Gee4Parser.RuleReferenceContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#specialRule}.
	 * @param ctx the parse tree
	 */
	void enterSpecialRule(Gee4Parser.SpecialRuleContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#specialRule}.
	 * @param ctx the parse tree
	 */
	void exitSpecialRule(Gee4Parser.SpecialRuleContext ctx);
	/**
	 * Enter a parse tree produced by {@link Gee4Parser#fragmentRule}.
	 * @param ctx the parse tree
	 */
	void enterFragmentRule(Gee4Parser.FragmentRuleContext ctx);
	/**
	 * Exit a parse tree produced by {@link Gee4Parser#fragmentRule}.
	 * @param ctx the parse tree
	 */
	void exitFragmentRule(Gee4Parser.FragmentRuleContext ctx);
}