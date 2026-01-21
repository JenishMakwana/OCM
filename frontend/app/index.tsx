import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  TextInput,
  Modal,
  ScrollView,
  ActivityIndicator,
  Alert,
  SafeAreaView,
  StatusBar,
  RefreshControl,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL;

interface Tyre {
  id: string;
  brand: string;
  size: string;
  type: string;
  pattern: string;
  stock: number;
  price: number;
}

export default function Index() {
  const [tyres, setTyres] = useState<Tyre[]>([]);
  const [filteredTyres, setFilteredTyres] = useState<Tyre[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedBrand, setSelectedBrand] = useState<string>('All');
  const [brands, setBrands] = useState<string[]>(['All']);
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedTyre, setSelectedTyre] = useState<Tyre | null>(null);
  const [newStock, setNewStock] = useState('');
  const [newPrice, setNewPrice] = useState('');

  useEffect(() => {
    fetchTyres();
    fetchBrands();
  }, []);

  useEffect(() => {
    filterTyres();
  }, [tyres, searchQuery, selectedBrand]);

  const fetchTyres = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/tyres`);
      const data = await response.json();
      setTyres(data);
      setLoading(false);
      setRefreshing(false);
    } catch (error) {
      console.error('Error fetching tyres:', error);
      Alert.alert('Error', 'Failed to load tyres');
      setLoading(false);
      setRefreshing(false);
    }
  };

  const fetchBrands = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/tyres/brands`);
      const data = await response.json();
      setBrands(['All', ...data.brands]);
    } catch (error) {
      console.error('Error fetching brands:', error);
    }
  };

  const filterTyres = () => {
    let filtered = tyres;

    // Filter by brand
    if (selectedBrand !== 'All') {
      filtered = filtered.filter((tyre) => tyre.brand === selectedBrand);
    }

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(
        (tyre) =>
          tyre.size.toLowerCase().includes(searchQuery.toLowerCase()) ||
          tyre.pattern.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    setFilteredTyres(filtered);
  };

  const openEditModal = (tyre: Tyre) => {
    setSelectedTyre(tyre);
    setNewStock(tyre.stock.toString());
    setNewPrice(tyre.price.toString());
    setModalVisible(true);
  };

  const handleUpdate = async () => {
    if (!selectedTyre) return;

    const stockValue = parseInt(newStock);
    const priceValue = parseFloat(newPrice);

    if (isNaN(stockValue) || isNaN(priceValue) || stockValue < 0 || priceValue < 0) {
      Alert.alert('Invalid Input', 'Please enter valid stock and price values');
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/api/tyres/${selectedTyre.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          stock: stockValue,
          price: priceValue,
        }),
      });

      if (response.ok) {
        Alert.alert('Success', 'Tyre updated successfully');
        setModalVisible(false);
        fetchTyres();
      } else {
        Alert.alert('Error', 'Failed to update tyre');
      }
    } catch (error) {
      console.error('Error updating tyre:', error);
      Alert.alert('Error', 'Failed to update tyre');
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    fetchTyres();
  };

  const renderTyreCard = ({ item }: { item: Tyre }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => openEditModal(item)}
      activeOpacity={0.7}
    >
      <View style={styles.cardHeader}>
        <View style={styles.brandBadge}>
          <Text style={styles.brandText}>{item.brand}</Text>
        </View>
        <View style={[styles.stockBadge, item.stock <= 5 ? styles.lowStock : null]}>
          <Text style={styles.stockText}>Stock: {item.stock}</Text>
        </View>
      </View>

      <View style={styles.cardBody}>
        <Text style={styles.sizeText}>{item.size}</Text>
        <Text style={styles.typeText}>{item.type}</Text>
      </View>

      <Text style={styles.patternText}>{item.pattern}</Text>

      <View style={styles.cardFooter}>
        <Text style={styles.priceText}>₹{item.price.toFixed(2)}</Text>
        <Ionicons name="create-outline" size={24} color="#007AFF" />
      </View>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar barStyle="light-content" />
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#007AFF" />
          <Text style={styles.loadingText}>Loading inventory...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Tyre Inventory</Text>
        <Text style={styles.headerSubtitle}>{filteredTyres.length} items</Text>
      </View>

      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <Ionicons name="search" size={20} color="#999" style={styles.searchIcon} />
        <TextInput
          style={styles.searchInput}
          placeholder="Search by size or pattern..."
          placeholderTextColor="#999"
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
        {searchQuery ? (
          <TouchableOpacity onPress={() => setSearchQuery('')}>
            <Ionicons name="close-circle" size={20} color="#999" />
          </TouchableOpacity>
        ) : null}
      </View>

      {/* Brand Filter */}
      <View style={styles.brandFilterContainer}>
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.brandFilter}
          contentContainerStyle={styles.brandFilterContent}
        >
          {brands.map((brand) => (
            <TouchableOpacity
              key={brand}
              style={[
                styles.brandButton,
                selectedBrand === brand ? styles.brandButtonActive : null,
              ]}
              onPress={() => setSelectedBrand(brand)}
            >
              <Text
                style={[
                  styles.brandButtonText,
                  selectedBrand === brand ? styles.brandButtonTextActive : null,
                ]}
              >
                {brand}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {/* Tyre List */}
      <FlatList
        data={filteredTyres}
        renderItem={renderTyreCard}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#007AFF" />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Ionicons name="albums-outline" size={64} color="#666" />
            <Text style={styles.emptyText}>No tyres found</Text>
          </View>
        }
      />

      {/* Edit Modal */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Update Tyre</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Ionicons name="close" size={28} color="#FFF" />
              </TouchableOpacity>
            </View>

            {selectedTyre && (
              <View style={styles.modalBody}>
                <View style={styles.tyreInfo}>
                  <Text style={styles.tyreInfoBrand}>{selectedTyre.brand}</Text>
                  <Text style={styles.tyreInfoSize}>{selectedTyre.size} - {selectedTyre.type}</Text>
                  <Text style={styles.tyreInfoPattern}>{selectedTyre.pattern}</Text>
                </View>

                <View style={styles.inputGroup}>
                  <Text style={styles.inputLabel}>Stock Quantity</Text>
                  <TextInput
                    style={styles.input}
                    keyboardType="numeric"
                    value={newStock}
                    onChangeText={setNewStock}
                    placeholder="Enter stock quantity"
                    placeholderTextColor="#999"
                  />
                </View>

                <View style={styles.inputGroup}>
                  <Text style={styles.inputLabel}>Price (₹)</Text>
                  <TextInput
                    style={styles.input}
                    keyboardType="decimal-pad"
                    value={newPrice}
                    onChangeText={setNewPrice}
                    placeholder="Enter price"
                    placeholderTextColor="#999"
                  />
                </View>

                <View style={styles.modalButtons}>
                  <TouchableOpacity
                    style={[styles.button, styles.cancelButton]}
                    onPress={() => setModalVisible(false)}
                  >
                    <Text style={styles.cancelButtonText}>Cancel</Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={[styles.button, styles.updateButton]}
                    onPress={handleUpdate}
                  >
                    <Text style={styles.updateButtonText}>Update</Text>
                  </TouchableOpacity>
                </View>
              </View>
            )}
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0F0F0F',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    color: '#FFF',
    fontSize: 16,
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 16,
    paddingBottom: 12,
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFF',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#999',
    marginTop: 4,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1C1C1E',
    marginHorizontal: 20,
    marginBottom: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
    height: 48,
  },
  searchIcon: {
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    color: '#FFF',
    fontSize: 16,
  },
  brandFilterContainer: {
    backgroundColor: '#0F0F0F',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#2C2C2E',
  },
  brandFilter: {
    maxHeight: 60,
  },
  brandFilterContent: {
    paddingHorizontal: 20,
    paddingVertical: 4,
    gap: 10,
  },
  brandButton: {
    paddingHorizontal: 24,
    paddingVertical: 12,
    backgroundColor: '#2C2C2E',
    borderRadius: 24,
    marginRight: 10,
    borderWidth: 2,
    borderColor: '#2C2C2E',
  },
  brandButtonActive: {
    backgroundColor: '#007AFF',
    borderColor: '#007AFF',
  },
  brandButtonText: {
    color: '#CCC',
    fontSize: 15,
    fontWeight: '700',
  },
  brandButtonTextActive: {
    color: '#FFF',
  },
  listContent: {
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  card: {
    backgroundColor: '#1C1C1E',
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  brandBadge: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 8,
  },
  brandText: {
    color: '#FFF',
    fontSize: 12,
    fontWeight: '700',
  },
  stockBadge: {
    backgroundColor: '#2C2C2E',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 8,
  },
  lowStock: {
    backgroundColor: '#FF3B30',
  },
  stockText: {
    color: '#FFF',
    fontSize: 12,
    fontWeight: '600',
  },
  cardBody: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  sizeText: {
    color: '#FFF',
    fontSize: 20,
    fontWeight: '700',
    marginRight: 12,
  },
  typeText: {
    color: '#999',
    fontSize: 14,
    fontWeight: '600',
  },
  patternText: {
    color: '#BBB',
    fontSize: 14,
    marginBottom: 12,
  },
  cardFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#2C2C2E',
    paddingTop: 12,
  },
  priceText: {
    color: '#34C759',
    fontSize: 24,
    fontWeight: '800',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyText: {
    color: '#666',
    fontSize: 16,
    marginTop: 16,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: '#1C1C1E',
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    paddingBottom: 40,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#2C2C2E',
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: '#FFF',
  },
  modalBody: {
    padding: 20,
  },
  tyreInfo: {
    backgroundColor: '#2C2C2E',
    padding: 16,
    borderRadius: 12,
    marginBottom: 24,
  },
  tyreInfoBrand: {
    color: '#007AFF',
    fontSize: 16,
    fontWeight: '700',
    marginBottom: 4,
  },
  tyreInfoSize: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 4,
  },
  tyreInfoPattern: {
    color: '#999',
    fontSize: 14,
  },
  inputGroup: {
    marginBottom: 20,
  },
  inputLabel: {
    color: '#FFF',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#2C2C2E',
    borderRadius: 12,
    padding: 16,
    color: '#FFF',
    fontSize: 16,
  },
  modalButtons: {
    flexDirection: 'row',
    gap: 12,
    marginTop: 8,
  },
  button: {
    flex: 1,
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  cancelButton: {
    backgroundColor: '#2C2C2E',
  },
  cancelButtonText: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: '600',
  },
  updateButton: {
    backgroundColor: '#007AFF',
  },
  updateButtonText: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: '700',
  },
});
