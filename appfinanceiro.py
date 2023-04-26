import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import investpy as inv
from datetime import date
import fundamentus as fd

def home():
    col1,col2,col3=st.columns(3)
    with col2:
        st.image('baixados.png')
        st.markdown('---')
        st.title('App Financeiro')
        st.markdown('---')
    

def panorama():
    st.title('Panorama do Mercado')
    st.markdown(date.today().strftime('%d/%m/%Y'))
    st.subheader('Mercados pelo Mundo')

    dict_tickers ={
        'Bovespa':'^BVSP',
        'SP&500':'^GSPC',
        'NASDAQ':'^IXIC',
        'DAX':'^GDAXI',
        'FTSE 100': '^FTSE',
        'Crude Oil':'CL=F',
        'Gold':'GC=F',
        'BTC':'BTC-USD',
        'ETH':'ETH-USD'
    }

    df_info=pd.DataFrame({'Ativo':dict_tickers.keys(),'Ticker':dict_tickers.values()})

    df_info['Preço']=''
    df_info['%']=''
    count=0
    with st.spinner('Baixando os dados do mercado...'):
        for ticker in dict_tickers.values():
            cotacoes=yf.download(ticker,period='5d')['Adj Close']
            variacao=(cotacoes.iloc[-1]/cotacoes.iloc[-2]-1)*100
            df_info['Preço'][count]=round(cotacoes.iloc[-1],2)
            df_info['%'][count]=round(variacao,2)
            count+=1
    


    

    col1,col2,col3=st.columns(3)

    with col1:
        st.metric(df_info['Ativo'][0],value=df_info['Preço'][0],delta=str(df_info['%'][0])+'%')
        st.metric(df_info['Ativo'][1],value=df_info['Preço'][1],delta=str(df_info['%'][1])+'%')
        st.metric(df_info['Ativo'][2],value=df_info['Preço'][2],delta=str(df_info['%'][2])+'%')

    with col2:
        st.metric(df_info['Ativo'][3],value=df_info['Preço'][3],delta=str(df_info['%'][3])+'%')
        st.metric(df_info['Ativo'][4],value=df_info['Preço'][4],delta=str(df_info['%'][4])+'%')
        st.metric(df_info['Ativo'][5],value=df_info['Preço'][5],delta=str(df_info['%'][5])+'%')

    with col3:
        st.metric(df_info['Ativo'][6],value=df_info['Preço'][6],delta=str(df_info['%'][6])+'%')
        st.metric(df_info['Ativo'][7],value=df_info['Preço'][7],delta=str(df_info['%'][7])+'%')
        st.metric(df_info['Ativo'][8],value=df_info['Preço'][8],delta=str(df_info['%'][8])+'%')


    st.markdown('---')

    st.subheader('Comportamento ao longo do dia')

    lista_ativos=dict_tickers.values()
    ativo=st.selectbox('Selecione o Ativo',lista_ativos)

    indice_diario=yf.download(ativo,period='1d',interval='5m')

    import plotly.graph_objects as go

    fig=go.Figure()

    fig.add_trace(go.Candlestick(x=indice_diario.index,open=indice_diario.Open,high=indice_diario.High,low=indice_diario.Low,close=indice_diario.Close))

    fig.update_layout(title=f'Gráfico Diário de {ativo}',
    template='simple_white',xaxis_rangeslider_visible=False)

    st.plotly_chart(fig)
    
    lista_acoes=['PETR4.SA','VALE3.SA','ITUB4.SA','WEGE3.SA','TAEE11.SA']
    acao=st.selectbox('Selecione a Ação',lista_acoes)

    preco=yf.download(acao,period='1d',interval='5m')

    import plotly.graph_objects as go

    fig=go.Figure()

    fig.add_trace(go.Candlestick(x=preco.index,open=preco.Open,high=preco.High,low=preco.Low,close=preco.Close))

    fig.update_layout(title=f'Gráfico Diário de {acao}',
    template='simple_white',xaxis_rangeslider_visible=False)

    st.plotly_chart(fig)

def mapa_mensal():
    st.title('Análise Retorno Mensal')

    with st.expander('Escolha entre Indices ou Ações',expanded=True):
        opcao=st.radio('Selecione',['Indices','Ações'])
    
    if opcao=='Indices':
        with st.form(key='form_indice'):
            ticker=st.selectbox('Indice',['^BVSP','^GSPC','^IFIX','BTC-USD'])
            analisar=st.form_submit_button('Analisar')
    else:
        with st.form(key='form_acao'):
            ticker=st.selectbox('Ações',['PETR4.SA','EQTL3.SA','VALE3.SA'])
            analisar=st.form_submit_button('Analisar')

    if analisar:
        data_ini='1999-12-01'
        data_fim='2023-04-01'

        if opcao=='Indices':
            retornos=yf.download(ticker,start=data_ini,end=data_fim,interval='1mo')[['Close']].pct_change()
        else:
            retornos=yf.download(ticker,start=data_ini,end=data_fim,interval='1mo')[['Close']].pct_change()

        retorno_mensal=retornos.groupby([retornos.index.year.rename('Year'),retornos.index.month.rename('Month')]).mean()

        tabela_retornos=pd.DataFrame(retorno_mensal)
        
        tabela_retornos=pd.pivot_table(tabela_retornos,values='Close',index='Year',columns='Month')
        tabela_retornos.columns=['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']

        fig,ax=plt.subplots(figsize=(12,9))

        cmap=sns.color_palette('RdYlGn',50)

        sns.heatmap(tabela_retornos,cmap=cmap,annot=True, fmt='.2%',center=0,vmax=0.02,vmin=-0.02,cbar=False,linewidths=1,xticklabels=True,ax=ax)

        ax.set_title(ticker,fontsize=18)

        ax.set_yticklabels(ax.get_yticklabels(),rotation=0,verticalalignment='center',fontsize='12')

        ax.set_xticklabels(ax.get_xticklabels(),fontsize='12')

        ax.xaxis.tick_top()
        
        plt.ylabel('')

        st.pyplot(fig)


        stats=pd.DataFrame(tabela_retornos.mean(),columns=['Média'])
        stats['Mediana']=tabela_retornos.median()
        stats['Máx']=tabela_retornos.max()
        stats['Min']=tabela_retornos.min()
        stats['Meses Positivos']=tabela_retornos.gt(0).sum()/tabela_retornos.count()
        stats['Meses Negativos']=tabela_retornos.le(0).sum()/tabela_retornos.count()
        

        stats_a=stats[['Média','Mediana','Máx','Min']]

        stats_a=stats_a.T


        fig,ax=plt.subplots(figsize=(9,2.5))

        cmap=sns.color_palette('RdYlGn',50)

        sns.heatmap(stats_a,cmap=cmap,annot=True, fmt='.2%',center=0,vmax=0.02,vmin=-0.02,cbar=False,linewidths=1,xticklabels=True,ax=ax)

        ax.set_title(ticker,fontsize=18)

        ax.set_yticklabels(ax.get_yticklabels(),rotation=0,verticalalignment='center',fontsize='12')

        ax.set_xticklabels(ax.get_xticklabels(),fontsize='12')

        ax.xaxis.tick_top()
        
        plt.ylabel('')

        st.pyplot(fig)


        tabela_b=stats[['Meses Positivos','Meses Negativos']]
        tabela_b=tabela_b.T

        fig,ax=plt.subplots(figsize=(9,2.5))

        cmap=sns.color_palette('RdYlGn',50)

        sns.heatmap(tabela_b,cmap=cmap,annot=True, fmt='.2%',center=0.5,vmax=1,vmin=0,cbar=False,linewidths=1,xticklabels=True,ax=ax)

        ax.set_title(ticker,fontsize=18)

        ax.set_yticklabels(ax.get_yticklabels(),rotation=0,verticalalignment='center',fontsize='12')

        ax.set_xticklabels(ax.get_xticklabels(),fontsize='12')

        ax.xaxis.tick_top()
        
        plt.ylabel('')

        st.pyplot(fig)



def fundamentos():
    st.title('Informações de Fundamentos')
    lista_tickers=fd.list_papel_all()
    
    comparar=st.checkbox('Compara 2 ativos')


    col1,col2=st.columns(2)

    with col1:
        with st.expander('Ativo 1',expanded=True):
            papel=st.selectbox('Selecione o Papel',lista_tickers)

            info=fd.get_detalhes_papel(papel)
            st.write('**Empresa**',info['Empresa'][0])
            st.write('**Setor**',info['Setor'][0])
            st.write('**Subsetor**',info['Subsetor'][0])
            st.write('**Valor de Mercado**',f"R$ {float(info['Valor_de_mercado'][0]):,.2f}")
            st.write('**Patrimônio Líquido**',f"R$ {float(info['Patrim_Liq'][0]):,.2f}")
            st.write('**EV/EBITDA**',f"{float(info['EV_EBITDA'][0])/100:,.2f}")
            st.write('**Dívida Bruta**',f"R$ {float(info['Div_Bruta'][0]):,.2f}")
            st.write('**Dívida Líquida**',f"R${float(info['Div_Liquida'][0]):,.2f}")
            st.write('**P/L**',f"{float(info['PL'][0])/100}")
            st.write('**Dividend Yield**',f"{info['Div_Yield'][0]}")


    if comparar:
        with col2:
            with st.expander('Ativo 2',expanded=True):
                papel2=st.selectbox('Selecione o Segundo Papel',lista_tickers)

                info2=fd.get_detalhes_papel(papel2)
                st.write('**Empresa**',info2['Empresa'][0])
                st.write('**Setor**',info2['Setor'][0])
                st.write('**Subsetor**',info2['Subsetor'][0])
                st.write('**Valor de Mercado**',f"R$ {float(info2['Valor_de_mercado'][0]):,.2f}")
                st.write('**Patrimônio Líquido**',f"R$ {float(info2['Patrim_Liq'][0]):,.2f}")
                st.write('**EV/EBITDA**',f"{float(info2['EV_EBITDA'][0])/100:,.2f}")                
                st.write('**Dívida Bruta**',f"R$ {float(info2['Div_Bruta'][0]):,.2f}")
                st.write('**Dívida Líquida**',f"R${float(info2['Div_Liquida'][0]):,.2f}")
                st.write('**P/L**',f"{float(info2['PL'][0])/100}")
                st.write('**Dividend Yield**',f"{info2['Div_Yield'][0]}")


               
                




def main():
    st.sidebar.image('baixados.png',width=200)
    st.sidebar.title('App Financeiro')
    st.sidebar.markdown('---')

    lista_menu=['Home','Panorama Mercado','Rentabilidades Mensais','Fundamentos']
    escolha=st.sidebar.radio('Escolha a opção',lista_menu)

    if escolha=='Home':
        home()
    elif escolha=='Panorama Mercado':
        panorama()
    elif escolha=='Rentabilidades Mensais':
        mapa_mensal()
    elif escolha=='Fundamentos':
        fundamentos()

main()